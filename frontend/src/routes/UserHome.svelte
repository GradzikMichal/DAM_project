<script>
    import {getCookieValue} from "../util.js";
    import {navigate} from "svelte5-router";

</script>

{#if getCookieValue("logged_in") === "True"}
<main>
    <div>
        <p>
            Nice
        </p>
    </div>
</main>
{:else}
    {navigate("/login")}
{/if}