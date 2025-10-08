<div align="center">

# Chanty
### Write Minecraft datapacks easely with Python

</div>

**chanty** is a Python DSL for writing Minecraft datapacks as if they were real code.  
No more messy `.mcfunction` files - just cliean, structured logic.


## Install
```
pip install chanty
```


## Usage

```py
from chanty import Datapack, Namespace, CommandBuilder

pack = DataPack('my_awesome_datapack')
namespace = Namespace('main')

@namespace.on_load
def handle_on_load() -> str:
    with CommandBuilder() as cmd:
        cmd.tellraw('Hello world from chanty datapack!')
    return cmd.build()


# Export into folder
pack.export('./my_datapack')
```
