from chanty.command.builder import CommandBuilder


def test_tellraw():
    with CommandBuilder() as cmd:
        cmd.say("hello world")
    assert cmd.build() == 'say hello world'
