from chanty import DataPack, Namespace, CommandBuilder
import src.translations

pack = DataPack('simple_project')
namespace = Namespace('main')
pack.register(namespace)


@namespace.on_load
def handle_on_load() -> str:
    with CommandBuilder() as cmd:
        cmd.tellraw("Hello from your Chanty project <3")
    return cmd.build()


if __name__ == "__main__":
    pack.export('./exported/simple_project')
