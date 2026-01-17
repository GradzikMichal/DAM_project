<script>
  import {Route, Router, Link, link, navigate} from "svelte5-router";
  import Login from "./routes/Login.svelte";
  import UserHome from "./routes/UserHome.svelte";
  let {url = ""} =$props();


</script>

<Router {url}>
  <nav>
    <Link to="/login">Login</Link>

    <Link to="/user-home">Home</Link>
  </nav>
  <div>
    <Route path="/login" replace><Login/></Route>
    <Route path="/user-home" replace>
        <UserHome/>
    </Route>
  </div>
</Router>