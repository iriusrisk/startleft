---
search:
  boost: 3 
---
---

This is a list of common pitfalls on using StartLeft, and how to avoid them.

### `ImportError: failed to find libmagic.`
---
When using Windows or OSX OS, there is the requirement to manually install the corresponding 
<a href="https://github.com/ahupp/python-magic" target="_blank">python-magic</a> 
library as indicated in the [prerequisites section](Quickstart-Guide-for-Beginners.md#prerequisites).

### `Cannot open include file: 'graphviz/cgraph.h'`
---
When using Windows, it is sometimes required to set up some extra configurations. 

Install Graphviz in your OS using the following command:
```shell
choco install graphviz
```

Adding the Graphviz binaries to the PATH
```shell
echo "C:\Program Files\Graphviz\bin" >> $PATH
```

Installing the `pygraphviz` lib setting the OS files location: 

```shell
pip install --global-option=build_ext --global-option="-IC:\Program files\Graphviz\include" --global-option="-LC:\Program files\Graphviz\lib" pygraphviz
```

### `pygraphviz/graphviz_wrap.c:154:11: fatal error: Python.h: No such file or directory`
Looks like you haven't properly installed the header files and static libraries for python dev.

You need to add a PPA offered by the 
<a href="https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa" target="_blank">“deadsnakes”</a>
team to get the old archived Python versions easily.

```shell
sudo apt install software-properties-common
```

```shell
sudo add-apt-repository ppa:deadsnakes/ppa
```

After you need to install the required library for your python dev version:

```shell
sudo apt install python3.x-dev
```
