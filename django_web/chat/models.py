import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class OllamaModel(models.Model):
    model_name = models.CharField(max_length=100, primary_key=True)
    model_alias = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.model_alias


class Conversation(models.Model):
    tag = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_name = models.ForeignKey(OllamaModel, on_delete=models.CASCADE, to_field="model_alias")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_message = models.TextField()

    def __str__(self):
        return str(self.tag)


class ModelUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    allowed_models = models.ManyToManyField(OllamaModel)

    def get_allowed_models(self):
        return "\n".join([o.model_alias for o in self.allowed_models.all()])

    def __str__(self):
        return str(self.user)
