<script>
    import {Carta, Markdown} from "carta-md";
    import {tick} from "svelte";

    let {csrf, chatTag=$bindable("new"), messages=$bindable([]), chatHistory=$bindable({}), chatModel=$bindable("")} = $props();
    let message_div  = $state();
    let new_message = $state("");
    const carta = new Carta();


    async function sendData(body){
        return await fetch("http://localhost:8080/api/chats/", {
            method: "POST",
            body: body.toString(),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "mode": "cors",
                "credentials": "same-origin",
                "cookie": document.cookie,
            }
        }).then(res => res.json());
    }
    function checkFetchParameters(){
        if (new_message === "") throw new Error("Message to the model is needed!")
        if (chatModel === "") throw new Error("LLM model not chosen!")
        if (chatTag === "") throw new Error("The conversation was not found!")
        if (csrf === "") throw new Error("The server error")
    }

    async function sendMessage(){
        try {
            checkFetchParameters();
            let body = new URLSearchParams({
                csrfmiddlewaretoken: csrf,
                message: new_message,
                model: chatModel,
                chatTag: chatTag,
            });
            messages.push({"role": "user", "content": new_message});
            new_message = ""
            document.getElementById("llm_loading").style.display = "grid";
            let response = await sendData(body);
            if (chatTag === "new"){
                chatTag = response["chatTag"];
                chatHistory["tags"].push(chatTag);
                chatHistory["models_names"].push(chatModel);
                chatHistory["first_messages"].push(new_message);
            }
            document.getElementById("llm_loading").style.display = "none";
            messages.push(response["response"]);
        } catch (error) {
            messages.pop()
            console.log(error);
        }
    }

    function vh(percent){
        let h = Math.max(document.documentElement.clientWidth, document.documentElement.clientHeight || 0);
        return (percent / h)/100;
    }

    $effect.pre(() =>{
        if(!message_div) return;
        messages.length;
        if (message_div.offsetHeight + message_div.scrollTop > message_div.scrollHeight - 50) {
            tick().then(()=>{
                message_div.scrollTop({
                    top: message_div.scrollHeight,
                    left:0,
                    behavior: "smooth"
                })
            })
        }
    });

    $effect(() => {
        if(!document.getElementById("chat")) return;
        new_message.length;
        let textarea = document.getElementById("chat");
        let height_diff = textarea.scrollHeight - textarea.offsetHeight;
        let difference = (height_diff <= 4) ? 44 : textarea.scrollHeight;
        textarea.style.height = difference.toString() + "px";

        textarea.offsetHeight;
        let chatHeight = difference > vh(30) ? vh(30) : difference;
        message_div.style.height = ((message_div.parentElement.offsetHeight * 18/20) - chatHeight - 2).toString() + "px";
        let button = document.getElementById("send");
        button.style.marginTop = (chatHeight - 44).toString() + "px";
    })

</script>

{#snippet  chatBubble(role, bubbleClass, message)}
<div class="chat chat-{role}">
    <div class="chat-bubble chat-bubble-{bubbleClass}">
        <Markdown value={message.content} {carta}/>
    </div>
</div>
{/snippet}

<div class="overflow-scroll h-18/20 mt-2 mb-2 ml-2 pr-2" bind:this={message_div}>
    <div>
        {#each messages as message}
            {#key messages}
                {#if message.role === "llm"}
                    {@render chatBubble("start", "primary", {message})}
                {:else}
                    {@render chatBubble("end", "secondary", {message})}
                {/if}
            {/key}
        {/each}
        <div class="chat chat-start" id="llm_loading" style="display:none">
            <div class="chat-bubble chat-bubble-primary">
                <span class="loading loading-dots loading-sm"></span>
            </div>
        </div>
    </div>
</div>
<div class="ml-auto mr-auto ms-auto w-19/20">
    <form class="w-19/20" id="form" action="javascript:void(0)">
        <div class="w-17/20 join-item join">
            <input type="hidden" name="csrfmiddlewaretoken" value={csrf}/>

            <textarea
                    bind:value={new_message}
                    id="chat"
                    placeholder="Message"
                    style="height: 38px !important;"
                    class="join-item rounded-md w-full p-3 field-sizing-content min-h-[38px] text-sm max-h-[30vh]
                     border border-gray-500 resize-none scroll-m-2 focus:border-zinc-400 focus:ring-0 focus:outline-none"></textarea>
        </div>
        <button class="btn btn-neutral join-item w-2/10" id="send" onclick={sendMessage}>Send
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
            </svg>
        </button>
    </form>
</div>
<div class="mr-[70px] ml-auto mt-2">

        <select id="model-select" class="select select-xs float-right w-1/5 select-info" bind:value={chatModel}>
            {#if chatModel === ""}
                <option disabled selected>Select model</option>
                {#each chatHistory.user_models as model}
                    <option value={model}>{model}</option>
                {/each}
            {:else}
                <option disabled selected value={chatModel}>{chatModel}</option>
            {/if}
        </select>

</div>
