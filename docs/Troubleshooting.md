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
