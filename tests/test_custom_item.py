from chanty import CustomItem, Item, CommandBuilder


def test_create_custom_item():
    item = CustomItem(Item.STICK)
    @item.on_right_click
    def handle_rigth_click() -> str:
        with CommandBuilder() as cmd:
            cmd.tellraw('stick was used!')
        return cmd.build()
