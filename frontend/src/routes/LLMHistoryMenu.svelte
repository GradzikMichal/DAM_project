<script>
    import ChatBox from "../lib/LLMChatBox.svelte";
    let {csrf} = $props();
    let chatTag = $state("new");
    let urlParams = $state(new URLSearchParams(window.location.search));
    let messages = $state([]);

    async function getHistory(){
        try{
            let resp = await fetch("http://localhost:8080/api/chats",
                {
                    method: "GET",
                }).then(res => res.json());
            csrf = resp['csrf'];
            return JSON.parse(
                '{\"'+decodeURIComponent(resp['user_history'])
                    .replaceAll("&", ',\"')
                    .replaceAll('=','\":')
                    .replaceAll("+", " ")
                    .replaceAll("'", "\"")+"}"
            )
        } catch(err){
            console.log(err);
            return null;
        }
    }

    async function getChatByTag(){
        let response = await fetch("http://localhost:8080/api/chats/?" + urlParams.toString(),
            {
                method: "GET",
            }).then(res => res.json()).then(data => JSON.parse(data["response"]))
        console.log(response)
        return await response;
    }

    async function getChat(){
        if (chatTag !== "new"){
            if (urlParams.has("chatTag")) {
                if(!(messages.length > 0)){
                    messages  = await getChatByTag();
                }
            }
        }
    }

    document.body.onclick = function(anEvent){
        let trg = anEvent.target;
        if (trg.classList.contains("conversation")){
            chatTag = trg.id;
            urlParams.set("chatTag", chatTag);
            getChat();
        }
    }
</script>

{#snippet conversation(chatTag, firstMessage, model)}
    <div class="card bg-base-100 w-96 shadow-sm conversation">
        <div class="card-body conversation" id={chatTag}>
            <h2 class="card-title conversation" id={chatTag}>{firstMessage}</h2>
            <p class="conversation" id={chatTag}>Chat id: {chatTag}</p>
            <p class="conversation" id={chatTag}>Model: {model}</p>
        </div>
    </div>
{/snippet}

<div class="drawer lg:drawer-open basis-3/10 h-19/20">
    {#await getHistory() then chatHistory}
        <input id="my-drawer-3" type="checkbox" class="drawer-toggle" />
        <div class="drawer-side">
            <ul class="menu bg-base-200 min-h-full w-80 p-4">
                {#each Array(chatHistory.tags.length) as _,i}
                    {@render conversation(chatHistory.tags[i], chatHistory.first_messages[i], chatHistory.models_names[i])}
                {/each}
            </ul>
        </div>
        <div class="drawer-content">
            <ChatBox models={chatHistory.user_models} csrf={csrf} bind:chatTag={chatTag} bind:messages={messages}/>
        </div>
    {/await}
</div>