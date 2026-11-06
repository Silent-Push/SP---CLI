# SP - CLI

The Silent Push CLI (Command Line Interface)

- [Requirements](#Requirements)

- [Installation](#Installation)

- [Usage](#Usage)

  - [Supported commands and sub-commands so far](#supported-commands-and-sub-commands-so-far)

  - [Options](#options)

- [Interactive mode](#interactive-mode)

  - [The load/unload command](#the-load-and-unload-command)

- [SPQL Commands](#spql-commands)

- [Scripting](#scripting)

  - [run_pyscript command](#runpyscript-command)

  - [run_script command](#runscript-command)

  - [Batch execution tips](#batch-execution-tips)

- [For Devs](#for-devs)

  - [Using the library](#using-the-library)

  - [Linting](#linting)

- [Support](#support)

## Requirements
- Python 3.9 or later with pip: https://www.python.org/downloads/
- Windows users only:
  - Microsoft Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

## Installation

`python3 -m pip install SilentPushCLI`

After installed, export your Silent Push API key to your terminal:
### Linux and MacOS users
```shell
export SILENT_PUSH_API_KEY=YOUR-API-KEY
```
### Windows Users
```shell
setx /m SILENT_PUSH_API_KEY YOUR-API-KEY
```
Restart your CMD - Command Prompt

There's a demo video if you need more detailed instructions https://youtu.be/d4WApEZcXFg

`sp --version` shows the installed version.

## Usage
Syntax:
```shell
sp COMMAND [SUB-COMMAND...] IOC [PARAMETER=VALUE...] [OPTION...]
```
Use the help verbose command to get a detailed list of the available commands:
```shell
sp help -v
```
Use the help flag on any command to get more details:
```shell
sp padns query a --help
```
Examples:
```shell
sp score ig.com
sp enrich ig.com -es
sp bulk_enrich ig.com x.com ibm.com -es
sp padns query a ig.com limit=2 sort=last_seen/- -t
```
### Supported commands and sub-commands so far
- score
- enrich
- bulk_enrich
- padns
  - query
    - any
    - anyipv4
    - anyipv6
    - a
    - aaaa
    - cname
    - mx
    - ns
    - ptr4
    - ptr6
    - soa
    - txt
  - answer
    - a
    - aaaa
    - cname
    - mx
    - mxhash
    - ns
    - nshash
    - ptr4
    - ptr6
    - soa
    - soahash
    - txt
    - txthash
  - search
    - ipdiversity
- spql (multiline commands)
  - feedsearch
  - websearch
- threatcheck
- bulk_threatcheck
- whoislive
- job
- load
- unload
### Options
- all commands
  - **-j, --json**: JSON output (default)
  - **-c, --csv**: CSV output
  - **-t, --tsv**: TSV output
  - **-h, --help**: show help
  - **-v, --verbose**: verbosity output

The output options can't be combined.

- enrich/bulk_enrich
  - **-e, --explain**: show details of data used to calculate the different scores in the response
  - **-s, --scan_data**: show details of data collected from host scanning
- threatcheck/bulk_threatcheck
  - **-d, --datasource**: the datasource to threat check, default to 'iofa'
  - **-q, --qtype**: the query type, default to 'name'
  - **-n, --with_cnames**: includes CNAME records in the threat check

## Interactive mode
We also have an interactive console, If you type 'sp' alone, it will enter the 'sp console' and you can type commands without preceding 'sp', example:
```shell
SP# score ig.com
{
  "domain": "ig.com",
  "sp_risk_score": 18,
  "sp_risk_score_explain": {
    "sp_risk_score_decider": "ns_reputation_score"
  }
}

SP# padns query a ig.com limit=1
{
  "records": [
    {
      "answer": "195.234.39.132",
      "count": 2681,
      "first_seen": "2021-04-17 03:47:18",
      "last_seen": "2024-08-16 12:11:22",
      "query": "ig.com",
      "type": "A"
    }
  ]
}
```

### The load and unload command
This command gives you the ability of switching the console to a specific context and loading that group of commands.
As an example, 'padns' contains various sub-commands, so you can do like:
```shell
SP# load padns
PADNS loaded
SP (PADNS)# query ns ig.com limit=1
{
  "records": [
    {
      "answer": "dns1.p09.nsone.net",
      "count": 5963,
      "first_seen": "2020-12-26 00:41:26",
      "last_seen": "2024-08-16 09:25:09",
      "nshash": "981275157feda43a53ff6d166de985ff",
      "query": "ig.com",
      "ttl": 172800,
      "type": "NS"
    }
  ]
}

SP (PADNS)# answer ns dns1.p09.nsone.net limit=1
{
  "records": [
    {
      "answer": "dns1.p09.nsone.net",
      "count": 138,
      "first_seen": "2024-01-27 21:23:33",
      "last_seen": "2024-08-16 13:42:25",
      "nshash": "9b484fe18c1a52f56775302e5be302f8",
      "query": "tumblersforyou.com",
      "ttl": 3600,
      "type": "NS"
    }
  ]
}

SP (PADNS)# unload padns
PADNS unloaded
```
You still can use any other command normally.

## SPQL Commands

SPQL commands are multiline, since they can be quite complex. Use single quotes to span the query along the lines,
example in interactive mode:

```shell
SP# websearch 'domain="ibm.com"
  AND scan_date > "2025-01-01"' -l 2 -tv
```

The same example but in a single line:

```shell
websearch 'domain="ibm.com" AND scan_date > "2025-01-01"' -l 2 -tv
```

## Scripting
### run_pyscript command
There are 2 special commands for executing scripts using the 'sp' command, so you can
easily use it in your projects, here's a simple python script example:
```python
# my_script.py
result = app('score ibm.com -t')
print(result.data)
```
and this is how you can execute it:
```shell
sp run_pyscript my_script.py
```
### run_script command
Also, you can create a file with batch commands one per line and easily execute them, let's suppose we have this file:
```text
# my_script.txt
padns query mx ig.com limit=2
score ig.com -c
```
and then you can execute this batch commands file with:
```shell
sp run_script my_script.txt
```
or you can simply redirect the input (like importing a database):
```shell
sp < my_script.txt
```
### Batch execution tips

As you might know already, one of the greatest joy of shell scripting is the ability of loading batch parameters from
files.
Here's one idea for the bulk_enrich command:
```shell
cat to_enrich.txt | xargs sp bulk_enrich
```

Everything inside to_enrich.txt file will be treated as one parameter for the bulk_enrich command, don't mix domains
with IPs though,
since the command will depend on the type of enrichment being executed.

## For Devs
### Using the library

If you need to use the library on your own, here some examples:
```python
from sp.main import main as sp

sp(['enrich ig.com'])
sp(['padns query ns ig.com limit=2'])
```
another way of doing the same
```python
from sp.main import App
from sp.common.utils import AppFileManager

app = App(application_manager=AppFileManager('my app'))
app.onecmd_plus_hooks('enrich ig.com')
print(app.last_result)
app.onecmd_plus_hooks('padns query ns ig.com limit=2')
print(app.last_result)
```

### Linting

The project uses [ruff](https://docs.astral.sh/ruff/), which also runs on GitLab CI. To lint before every commit, enable
the git hook once per clone:

```bash
pip install -r requirements-dev.txt
git config core.hooksPath .githooks
```

## Support

Don't hesitate to contact me at [jorgeley@silentpush.com](mailto:jorgeley@silentpush.com) if you need any help
