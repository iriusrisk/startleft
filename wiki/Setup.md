Start by downloading Startleft via pip:

```
pip install git+https://github.com/iriusrisk/startleft.git
```
##Setup (CLI mode only)
You'll need to export two enviroment variables. The first is the IriusRisk server which should include protocol and hostname (with optional port) but not path. The second is your API token.

```
$ export IRIUS_SERVER=https://instance.iriusrisk.com
$ export IRIUS_API_TOKEN=123-123-123-123-123
```
The alternative is to include those values as command-line parameters `--irius-server` and `--api-token`, respectively.