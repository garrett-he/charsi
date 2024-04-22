<div align="center">
    <img src="https://raw.githubusercontent.com/garrett-he/charsi/main/docs/images/logo.png"/>
</div>

![license](https://img.shields.io/github/license/garrett-he/charsi)
![build](https://img.shields.io/github/actions/workflow/status/garrett-he/charsi/ubuntu-jammy.yml)
![codecov](https://img.shields.io/codecov/c/github/garrett-he/charsi)
![version](https://img.shields.io/pypi/v/charsi)
![python](https://img.shields.io/pypi/pyversions/charsi)
![downloads](https://img.shields.io/pypi/dm/charsi)

# Charsi

A command-line tool to help game modders build string resources
for [Diablo II: Resurrected][1].

## Introduction

In the classic version of Diablo II, there was a very famous hacking tool called
[Maphack][2], which could easily configure texts displayed in game. Now in
Diablo II: Resurrected, you can directly modify the JSON files to change texts
in game, but the workload is high, and it's easy to make mistakes.

![charsi-icon](./docs/images/charsi-icon.png) [Charsi][3] is the blacksmith in
the Rogue Encampment in Act I of Diablo II, and can imbue any normal item of the
player's choice.

This tool named **charsi**, can imbue game strings with your recipes which are
in a format similar to Maphack configurations.

## Quickstart

1. Extract `item-names.json` file at `/data/local/lng/strings` from game data
   storage by [CascView](http://www.zezula.net/en/casc/main.html).

2. Write a recipe file `example.recipe` with following:

```
Text[qf1]: Example
```

3. Run the following command to build a new string table:

```
charsi build --recipe-file=example.recipe item-names.json > new-item-names.json
```

4. Replace file `/data/local/lng/strings/item-names.json`
   with `new-item-names.json` in your mods.

5. Check in game, item name `Khalim's Flail` has been replaced with `Example`.

## How to Use

There are three concepts in Charsi: **String Table**, **Instruction** and
**Recipe**.

### String Table

Represents JSON files extracted from game data, the target for modding.

### Instruction

Tells Charsi what to do when building string tables, is equivalent to a
configuration in the `d2maphack.cfg`.

Format of instructions is:

```
name[query][language]: arg1, arg2, ...
```

* name: Name of instruction
* query: Specify which strings to operate on
* language: Optional, specify which language to operate on
* arg1, arg2, ...: Arguments of instruction, separated by comma

Three ways to query strings:

1. Single string:
   ```
   Instruction[qf1]: ... # for Khalim's Flail
   ```

2. By range:
   ```
   Instruction[qf1~qhr]: ... # all Khalim's stuffs
   ```

3. Discrete
   ```
   Instruction[qey, qhr]: ... # Khalim's Eye and Heart
   ```

**Built-in Instructions**

* `Text`: Replace string texts
* `Color`: Set color of string text

**Customize Instructions**

Instructions are implemented by Lua scripts and put in directory `/instructions`

**APIs for Lua to implement instructions**

* `RegisterInstruction(name, fn)`: Register a new instruction.
* `UnregisterInstruction(name)`: Unregister an existing instruction.
* `InstructionRegistered(name)`: Check whether instruction is registered.

### Recipe

A collection of instruction for building string tables.

#### Recipe Tags

You can set tags of recipes in format:

```
## Tag-name: value
```

`## Language`: The default language of instructions in this recipe

### Commands

Build a string table with recipe:

```
charsi build --recipe-file=/path/to/recipe path/to/stringtable
```

Build string tables with manifest files:

```
charsi build-manfiest path/to/manifest
```

### Manifest

In JSON format like:

```json
[
    {
        "input": "/path/to/stringtable",
        "output": "/path/to/output",
        "recipes": [
            "/path/to/recipe1",
            "/path/to/recipe2",
            "..."
        ]
    }
]
```

### Directory Structure

* `/instructions/`: Lua scripts for instruction handlers

### Variables

* `{origin}`: Placeholder for original text

### Alias

You can set alias to a bunch of keys by putting files in `/alias/`.

## License

Copyright (C) 2022 Garrett HE <garrett.he@hotmail.com>

The GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).

[1]: https://diablo2.blizzard.com

[2]: https://diablo2.diablowiki.net/Maphack

[3]: https://diablo.fandom.com/wiki/Charsi
