from chanty import CommandBuilder, Item
from chanty.command.condition import If, Unless


def test_base_conditions():
    with CommandBuilder() as cmd:
        with cmd.context(as_='@p') as me:
            hasnt_stick = Unless(me.inventory.has_in_inventory(Item.STICK))
            has_apple = If(me.inventory.has_in_inventory(Item.APPLE))
            with cmd.context(condition=hasnt_stick | has_apple):
                cmd.say('hello')
    code = cmd.build()
    print()
    print(code)
