# SP - CLI
The Silent Push Command Line Interface

## Installation
Download the python wheel from https://labs.silentpush.com/jorgeley/
and then install it with pip:
```shell
python3 -m pip install sp-0.0.1-py3-none-any.whl
```
After installed, export your Silent Push API key to your terminal:
```shell
export SILENT_PUSH_API_KEY=YOUR-API-KEY
```

## Usage
```shell
sp COMMAND [SUB-COMMAND...] IOC [PARAMETER=VALUE...] [OPTION...]
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
- load
### Options
- all commands
  - **-j, --json**: JSON output (default)
  - **-c, --csv**: CSV output
  - **-t, --tsv**: TSV output
  - **-h, --help**: show help
- enrich/bulk_enrich
  - **-e, --explain**: show details of data used to calculate the different scores in the response
  - **-s, --scan_data**: show details of data collected from host scanning

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

SP#
```

### The load/unload command
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
SP#
```
You still can use any other command normally.

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
As you might know already, the greatest feature of shell scripting is the ability of loading batch parameters from files.
Here's one idea for the bulk_enrich command:
```shell
cat to_enrich.txt | xargs sp bulk_enrich
```
Everything in to_enrich.txt file will be treated as one parameter for the bulk_enrich command, don't mix domains with IPs though, 
since the command will depend on the type of enrichment being executed.

## For Devs
### Using the library
I you need to use the library on your own, here some examples:
```python
from sp.sp import main as sp

sp(['enrich ig.com'])
sp(['padns query ns ig.com limit=2'])
```
another way of doing the same
```python
from sp.sp import App
from sp.common.utils import AppFileManager

app = App(application_manager=AppFileManager('my app'))
app.onecmd_plus_hooks('enrich ig.com')
print(app.last_result)
app.onecmd_plus_hooks('padns query ns ig.com limit=2')
print(app.last_result)
```

### Extending the commands - Guidelines
The commands are stored in the sp/commands directory, you can add more commands there, follow the existing ones as example.
The main library used for the project is [CMD2](https://cmd2.readthedocs.io/).
If you want to extend the commands, follow these steps:
1. create your new command python file inside sp/commands directory
2. follow the pattern of the
existing ones inside the same directory, per example, look at the [enrich.py](sp/commands/enrich.py), basically you need to
follow this template:
```python
@with_default_category("My New Category")
class MyNewCommandSet(BaseCommandSet):
  my_new_parser = BaseCommandSet._get_arg_parser()
  my_new_parser.add_argument("-s", "--some_argument")
  
  @with_argparser(my_new_parser)
  def do_something(self, params: Statement):
    with self.MyNewCommand(params, self) as my_new_command:
      my_new_command.something()
  
  class MyNewCommand(BaseCommand):
    
    def __enter__(self):
      # use this method if you need anything done before executing the command
      super().__enter__()
      return self

    def something(self):
      # your logic goes here, important to assign the response
      self._response = {"result": "your command result"}
    
    def __exit__(self, exc_type, exc_val, exc_tb):
      # use this method if you need anything done after executing the command
      super().__exit__(exc_type, exc_val, exc_tb)
```
3. add your new command to the commands package in the [sp/commands/\_\_init\_\_.py](sp/commands/__init__.py):
```python
# after the existing imports
from .my_new_command.py import *
```
4. add your new command to the initial loaded commands in [sp/settings.py](sp/settings.py):
```python
def get_initial_commands():
    from sp.commands import (
        # other imports
        MyNewCommandSet
    )
    # the available initial commands
    return {
        # other commands
        MyNewCommandSet(),
    }
```

That's it, your new command should be available, try `sp your_command --help`

## Support
Don't hesitate to contact me at [jorgeley@silentpush.com](jorgeley@silentpush.com) if you need any help