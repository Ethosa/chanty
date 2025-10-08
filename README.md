<div align="center">

# Chanty
### Write Minecraft datapacks easely with Python

</div>

**chanty** is a Python DSL for writing Minecraft datapacks as if they were real code.  
No more messy `.mcfunction` files - just cliean, structured logic.


## Install
```shell
pip install chanty
```


## CLI Usage

### Creating Project
```shell
chanty create test-project

cd test-project
```

### Build Datapack
for default `.minecraft` folder destionation:
```shell
chanty build --world_name="New World"
```

for ModrinthApp:
```shell
chanty build --modrinth="ProfileName:New World"
```

for other destination:
```shell
chanty build --to="./builds/datapack"
```


export to `./builds/<datapack_name>` folder:
```shell
chanty build --output="./builds"
```



## Usage

### Simple example
```py
from chanty import Datapack, Namespace, CommandBuilder

pack = DataPack('my_awesome_datapack')
namespace = Namespace('main')

@namespace.onload
def handle_onload() -> str:
    with CommandBuilder() as cmd:
        cmd.tellraw('Hello world from chanty datapack!')
    return cmd.build()


# Export into folder
if __name__ == '__main__':
    pack.export('./my_datapack')
```


### Custom Items
```py
from chanty import DataPack Namespace, CommandBuilder, CustomItem, Item


pack = DataPack('my_awesome_datapack')
namespace = Namespace('main')

my_cool_item = CustomItem(Item.STICK)
my_cool_item.set_name('§6§l[Chanty]§f§r Debugger')
my_cool_item.set_lore(
    'This is a not just stick ...',
    'This is a §6§l[Chanty]§f§r Debugger!',
)
my_cool_item.glint(True)
@my_cool_item.on_right_click
def handle_right_click():
    with CommandBuilder() as cmd:
        cmd.say('Hello!')
    return cmd.build()

namespace.register(my_cool_item)

if __name__ == '__main__':
    pack.export('./my_datapack')
```


## In The Future ...

- Assets
- Translations
- More built-in event handlers
- CLI improvement
