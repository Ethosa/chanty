from chanty import DataPack


def test_datapack_export():
    pack = DataPack('my awesome datapack')
    pack.export('./exported/my_awesome_datapack')
