Title: F# development without Visual Studio (in OS X)
Date: 2016-04-07 6:00
Category: blog

For my first article, I will talk about the technologies I am using to do side project with F# without Visual Studio.
While I focus on OS X, most of it is applicable with Linux (and Windows!). I choose this subject as I did not have a lot of knowledge of the .NET ecosystem
and most tutorials cover mostly Windows.


## Why F# ?
I decided to try to use F# when deciding to learn a functional language. F# seemed to me like a user-friendly OCaml with better tooling, ecosystem and documentation.

The argument could also be made that .NET is tied to Microsoft, but F# seems to be mostly driven by its community with awesome projects and tooling.


## Setup
Installing F# on OS X is surprisingly easy with Homebrew and gives you all the standard tools you need:
`fsharpc`, `fsharpi`, `mono`, `xbuild`
```bash
brew install mono
```

### Editor / IDE
A few options are open to you here. If you prefer a more "Visual Studio" development, Xamarin Studio is an excellent choice. Otherwise, Vim and Emacs have excellent bindings.

With this in mind, I decided to use [Ionide](http://ionide.io/) with [Visual Studio Code](https://code.visualstudio.com/) for its ease of use and the "no-setup required" while having great `IntelliSense`.

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
With F#, you don't even need a project to start with! If you prefer small scripting, the language use `.fsx` files.

An example script :
```fsharp
(* .fsx file example *)
#r "./packages/<pck>/lib/<.net>/<pck>.dll"  // import a .dll into .fsx
#load "regularfile.fs"                      // import .fs file into .fsx

printfn "Hello world!"
```

An F# dev will make quick use of its REPL (fsi) to test their code!
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

In Visual Studio, creating and managing solution is easy with the abstraction of `MSBuild` by the IDE.
Without it, it is somewhat painful, here is how I deal with projects.

#### Create solution / project
Using [Yeoman](http://yeoman.io/) with [generator-fsharp](https://github.com/fsprojects/generator-fsharp), choose "Empty Solution" with Paket and FAKE integration (more on those later).
Add subsequent projects by the same principle choosing between _Class Library_ (PCL profile 259 is a better choice for portability but some library like _FsUnit_ might not compile for now)
or _Console Application_ depending if you want an executable or not.

#### Using `.fsproj` files
To add files to the compiling, find the `Compile` targets and add your file (remember, compiling order is important in F#)
```xml
<ItemGroup>
    <Compile Target="myproject.fs" />
    ...
</ItemGroup>
```
For single project, this is the most you will have to interact with MSBuild. However, if you like to cross-reference projects here is how to do it:
```xml
<ItemGroup>
    <Reference Include="mscorlib" />
    ...

    <ProjectReference Include="..\core\core.fsproj">
      <Project>{99745828-ACF5-4B1B-8301-78F8345EB1CC}</Project> <!-- optional -->
      <Name>core</Name> <!-- optional -->
    </ProjectReference>
</ItemGroup>
```
Just add this `ProjectReference` linking to another sub-project and voilà, you can now compile with no headaches!
> Ionide (using F# Completion Tools) use the .fsproj files for the auto-completion

#### External libraries
Remember Paket? This is how we are going to manage external (NuGet probably) dependencies.
See their [Getting started](https://fsprojects.github.io/Paket/getting-started.html) to learn how to use it.

If you can't compile, it is because the package is not referenced in your project :

| Method   | Command |
| -------- | ------- |
| Ionide   | `Paket: Add NuGet (to current project)`                          |
| Terminal | `mono .paket/paket.exe add nuget <package> project <myproject>`  |

#### Compile
```bash
./build.sh        # runs default build profile
./build.sh Clean  # runs clean profile
```
Wait... that easy? No XBuild/MSBuild?
This is a script that was inserted by the Yeoman project template. It calls both Paket and FAKE to compile your project.

Speaking of FAKE, go read their [documentation](http://fsharp.github.io/FAKE/gettingstarted.html), but it is basically a build system using F# (much easier to use than MSBuild).


## Conclusion
I hope you liked this article. I feel that getting F# up and running in Linux (without previous knowledge of MSBuild or .NET in general)
is not straightforward and hopefully this can be a small reference on how to get it setup.


## Useful resources
 - F# Foundation
 - F# for Fun and Profit
 - F# Wikibook