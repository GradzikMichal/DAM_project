<script>
  import {Route, Router, Link, } from "svelte5-router";
  import Login from "./routes/Login.svelte";
  import UserHome from "./routes/UserHome.svelte";
  import Chat from "./routes/LLMHistoryMenu.svelte"
  let {url = ""} =$props();

</script>

<Router {url}>
  <div class="navbar bg-base-100 shadow-sm max-h-1/20">
    <div class="flex-1">
      <Link to="/user-home">Home</Link>
    </div>
    <div class="flex-none">
      <ul class="menu menu-horizontal px-1">
        {#if getCookieValue("logged_in") !== "True"}
          <li>
            <Link to="/login">
              Login
            </Link>
          </li>
          {:else}
          <li>
            <Link to="/llm">
              Chat bot
            </Link>
          </li>
          <li>
            <Link to="/logout">
              Logout
            </Link>
          </li>
          {/if}
      </ul>
    </div>
  </div>
  <div class="max-h-19/20">
    <Route path="/user-home" replace>
      <UserHome/>
    </Route>
    {#if getCookieValue("logged_in") !== "True"}
      <Route path="/login" replace><Login/></Route>
    {:else}
      <Route path="/llm" replace component={Chat}/>
    {/if}
  </div>
</Router>