---
search:
  boost: 3 
---
---

This is a list of common pitfalls on using StartLeft, and how to avoid them.

### `ImportError: failed to find libmagic.`
When using Windows or OSX OS, there is the requirement to manually install the corresponding 
<a href="https://github.com/ahupp/python-magic" target="_blank">python-magic</a> 
library as indicated in the [prerequisites section](Quickstart-Guide-for-Beginners.md#prerequisites).
---

### `"glightbox" package is not installed` 
When trying to launch StartLeft documentation by `mkdocs serve` using IntelliJ, you may get an 
error stating that the `glightbox` package is not installed. 

This requires re-running the `pip install -e ".[doc]"` 
command and restarting the IDE.
---