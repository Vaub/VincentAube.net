Title: F# development without Visual Studio
Subtitle: Exploration of tooling focusing on OS X
Date: 2016-04-07 6:00
Category: blog

For my first article, I will talk about the technologies I am using to do side project with F# without Visual Studio.
While I **focus on OS X**, most of it is applicable with Linux (and Windows!). I chose this subject as I did not have a lot of knowledge of the .NET ecosystem
and most tutorials cover Windows.


## Why F# ?
I started to use F# when deciding to learn a functional language. It seemed to be a "more" user-friendly OCaml with better tooling, ecosystem and documentation.

The argument could also be made that .NET is tied to Microsoft, but F# seems to be mostly driven by its community with awesome projects!


## Setup

### Installation
Installing F# on OS X is surprisingly easy with Homebrew and gives you all the standard tools you need:
`fsharpc`, `fsharpi`, `mono`, `xbuild`
```bash
brew install mono
```
#### General guides
 - [Mac](http://fsharp.org/use/mac/)
 - [Windows](http://fsharp.org/use/windows/)
 - [Linux](http://fsharp.org/use/linux/)

### Editor / IDE
A few options are open to you here:

 - [Xamarin Studio](https://www.xamarin.com/studio) (full IDE)
 - [Vim](https://github.com/fsharp/vim-fsharp)
 - [Emacs](https://github.com/fsharp/emacs-fsharp-mode) (very well supported)
 - [Sublime Text](https://github.com/fsharp/sublime-fsharp-package)
 - [Ionide Suite](http://ionide.io/) (using [Atom](https://atom.io) or [Visual Studio Code](https://code.visualstudio.com/))

With this in mind, I decided to go for Visual Studio Code for its "no-setup" and great IntelliSense


My VSCode settings (F# needs whitespace instead of `<Tab>`):
```json
{
  "editor.fontFamily": "Consolas",
  "editor.fontSize": 12,
  "editor.tabSize": 4,
  "editor.insertSpaces": true
}
```


## Starting a project
With F#, you don't even need a project to start with! If you prefer small scripting, the language uses `.fsx` files.

An example script :
```fsharp
(* .fsx file example *)
#r "./packages/<pck>/lib/<.net>/<pck>.dll"  // import a .dll into .fsx
#load "regularfile.fs"                      // import .fs file into .fsx

(* Copy from here in fsharpi if you want to try! *)
type HelloWorldState = | Hello | World | End

let changeState state =
    match state with
    | Hello -> World
    | World -> End
    | End   -> End

let printState state =
    match state with
    | Hello -> "Hello"
    | World -> "World"
    | End   -> ""

let rec writeHelloWorld state =
    match state with
    | End -> "!"
    | _   ->
        let nextState = changeState state
        (printState state) + " " + (writeHelloWorld nextState)

printfn "Output: %s" (writeHelloWorld Hello)
```

An F# dev will make quick use of its REPL to test their code!
```bash
fsharpi                 # open REPL
fsharpi myscript.fsx    # run the script in the REPL

# You can even compile your .fsx !
fsharpc myscript.fsx    # outputs myscript.exe, to be run with mono myscript.exe
```
With Ionide, you can send your script directly to `fsi` by opening the command palette and `FSI: Send file`
or selecting the code you want to send and `<Alt> + <Enter>`

### Larger project (multi-project)
However, if you are making a bigger project, chances are you need better tooling.

In Visual Studio, creating and managing solution is easy with abstracting `MSBuild`.
We sadly do not have this luck, here is how I deal with projects as someone who never really learned MSBuild.

#### Create solution / project
Download [Forge](http://fsprojects.github.io/Forge/) CLI tool or, using Yeoman, [generator-fsharp](https://github.com/fsprojects/generator-fsharp).

Here are my suggestions for projects templates:
```bash
$ forge new
Enter project name:
> YourProjectName

Enter project directory (relative to working directory):
> .                     # if you are in /usr/home , then the project will be in /usr/home/YourProjectName

Choose a template:
 - aspwebapi2
 - classlib             # normal class library, .NET Framework
 - console              # best template for .exe, you can always import libraries later
 - fslabbasic
 - fslabjournal
 - pcl259               # portable class library (.NET 4.5, WP8.1, WP8, Silverlight), might not work with all libraries
 - servicefabrichost
 - servicefabricsuavestateless
 - sln                  # creates an empty solution
 - suave
 - suaveazurebootstrapper
 - websharperserverclient
 - websharperspa
 - websharpersuave
 - windows

>

```
If you want multi project solution, `cd mySlnFolder` and re-run `forge new` in it

#### Using `.fsproj` files
To add files to the project, find the `Compile` targets and add your file (remember, compiling order is important in F#)
```xml
<ItemGroup>
    <Compile Target="myproject.fs" />
    ...
</ItemGroup>
```
For a single project, this is the most you will have to interact with MSBuild. However, if you like to cross-reference projects here is how to do it:
```xml
<ItemGroup>
    <Reference Include="mscorlib" />
    ...

    <ProjectReference Include="..\ProjectName\ProjectName.fsproj">
      <Project>{MY_UUID}</Project> <!-- optional -->
      <Name>ProjectName</Name> <!-- optional -->
    </ProjectReference>
</ItemGroup>
```
Just add this `ProjectReference` linking to another sub-project and voilà; you can now compile with no headaches!
> Ionide (using F# Compiler Service) uses the .fsproj files for auto-completion

#### External libraries
Remember Paket? This is how we are going to manage external (probably NuGet) dependencies.
See their [Getting started](https://fsprojects.github.io/Paket/getting-started.html) to learn how to use it.

If you can't compile, it is because the package is not referenced in your project :

| Method   | Command |
| -------- | ------- |
| Ionide   | `Paket: Add NuGet (to current project)`                |
| Terminal | `forge paket add nuget <package> project <myproject>`  |
You can also find Paket in `.paket` folder, so `mono .paket/paket.exe ...` without Forge


#### Compile
```bash
./build.sh        # runs default build profile
./build.sh Clean  # runs clean profile
```
Wait... that easy? No XBuild/MSBuild?
This is a script that was inserted by the Forge template. It calls both Paket and FAKE to compile your project.

Speaking of FAKE, go read their [documentation](http://fsharp.github.io/FAKE/gettingstarted.html)
but it is basically a build system using F# (much easier to use than MSBuild).


## Conclusion
I hope you liked this article. I feel that getting F# up and running in OS X (without previous knowledge of MSBuild or .NET in general)
is not that straightforward and hopefully this can be a small reference on how to get it setup.
I will update it in the future as the technology gets better (hopefully).


## Useful resources
 - [F# Foundation](https://fsharp.org)
 - [F# for Fun and Profit](https://fsharpforfunandprofit.com/) - Excellent tutorials
 - [F# Wikibook](https://en.wikibooks.org/wiki/F_Sharp_Programming) - Great references
 - [F# Cheatsheet](https://dungpa.github.io/fsharp-cheatsheet/) - Quicker references!

### Libraries I like
 - [Suave](http://suave.io) - Small (awesome) async and performant web server
 - [FSharp.Data](http://fsharp.github.io/FSharp.Data/) - Libraries for Data maniplation with types provider and parsers
 - [FsCheck](https://fscheck.github.io/FsCheck/) - "Random-testing" framework for testing a program specification