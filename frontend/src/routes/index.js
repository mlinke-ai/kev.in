import Home from "./Home.svelte"
import Profile from "./Profile.svelte"
import Error from "./Error.svelte"
import CodeSandbox from "./CodeSandbox.svelte"
//import ExamplePage from "./Example.svelte"

export default {
    "/": Home,
    "/profile": Profile,
    "/sandbox": CodeSandbox,
    //"/example-path": <ExamplePage>,
    "*": Error
}