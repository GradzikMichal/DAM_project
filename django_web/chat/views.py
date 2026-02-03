import json

import django.middleware.csrf
from urllib.parse import unquote
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from redisvl.extensions.message_history import MessageHistory

from django_web.chat.models import Conversation, OllamaModel
from django_web.dam_site import settings


# Create your views here.
def conversations_to_context(conversations: list[dict[str, str]]) -> dict[str, list[str]]:
    converted_conversations: dict[str, list[str]] = dict(
        tags=[],
        models_names=[],
        first_message=[]
    )
    for conversation in conversations:
        converted_conversations['tags'].append(str(conversation['tags']))
        converted_conversations['models_names'].append(conversation['models_names_id'])
        converted_conversations['first_message'].append(conversation['first_message'])
    return converted_conversations


def is_chat_user(user: User) -> bool:
    return user.groups.filter(name__endswith='chat').exists()


def user_message(message: str) -> dict[str, str]:
    return {
        "role": "user",
        "content": message,
    }


def open_message_history(chat_tag: str):
    return MessageHistory(
        name="chat_history",
        session_tag=chat_tag,
        redis_url=settings.REDIS_URL,
    )


@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(is_chat_user, login_url='/login')
def chats_history(request):
    if request.method == 'GET':
        csrf = django.middleware.csrf.get_token(request)
        user_conversations = Conversation.objects.filter(user_id=request.user.id).all().values()
        converted_conversations: dict[str, list[str]] = conversations_to_context(list(user_conversations))
        converted_conversations['user_models'] = request.user.modeluser.get_allowed_models().split('\n')
        return JsonResponse({"csrf": csrf, "user_history": converted_conversations}, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(is_chat_user, login_url='/login')
def chat_messages(request):
    if request.method == 'GET':
        chat_tag = request.GET.get('chat_tag', None)
        if chat_tag:
            if Conversation.objects.filter(user_id=request.user.id).filter(tags=chat_tag).exists():
                chat_history = open_message_history(chat_tag)
                recent_messages = chat_history.get_recent(
                    top_k=10,
                    raw=False,
                    session_tag=chat_tag,
                    role=["user", "llm"]
                )
                return JsonResponse(recent_messages, safe=False)
            return JsonResponse({"error": "Chat not found"}, status=403)
        return JsonResponse({"error": "Missing parameter!"}, status=422)
    elif request.method == 'POST':
        body = request.body.decode('utf-8')
        body = json.loads(body)
        chat_tag = body.get('chat_tag', None)
        model = body.get('model_name', None)
        message = unquote(body.get('message', None))
        if chat_tag and model and message:
            new_message = {"user": message}
            if chat_tag == "new":
                conversation = Conversation.objects.create(
                    user_id=User.objects.get(username=request.user.id),
                    model_name=OllamaModel.objects.get(model_alias=model),
                    first_message=message
                )
                chat_tag=str(conversation.tag)
            new_message["chat_tag"]=chat_tag
            new_message["model"]=model
            llm_response=send_message({
                "llm_type":"chat",
                "user_content":new_message
            })
            chat_history=open_message_history(chat_tag)
            chat_history.store(message, llm_response, chat_tag)
            if body.get("chat_tag", None) == "new":
                return JsonResponse({
                    "chat_tag": chat_tag,
                    "role": "llm",
                    "content": llm_response
                })
            else:
                return JsonResponse({
                    "role": "llm",
                    "content": llm_response
                })
        return JsonResponse({
            "error": "Data is missing!"
        }, status=422)
    elif request.method=="DELETE":
        chat_tag = request.GET.get("chat_tag", None)
        try:
            Conversation.objects.filter(user_id=request.user.id).filter(tag=chat_tag).delete()
            chat_history = open_message_history(chat_tag)
            messages = chat_history.get_recent(top_k=1000, raw=True)
            for message in messages:
                chats_history.drop(message['entry_id'])
            return HttpResponse(status=204)
        except Conversation.DoesNotExist:
            return HttpResponse(status=404)
