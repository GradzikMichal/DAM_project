<script>
    async function getCors(){
        try{
            const cors = await fetch("http://localhost:8080/api/login", {method:"GET"});
            const result = await cors.json();
            return result['csrf']
        }catch(err){
            console.log(err)
        }
    }

</script>

<main>
    <div>
        <form method="post" action="http://localhost:8080/api/login">
            <fieldset>
                <legend>Log in</legend>
                {#await getCors() then value}
                    <input type="hidden" name="csrfmiddlewaretoken" {value} />
                {/await}
                <label for="username">Username</label>
                <input type="text" id="username" name="username" placeholder="Username" />

                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Password" />

                <input type="submit" value="Log in"/>

            </fieldset>
        </form>
    </div>

</main>