import os
import mxgames


def is_game(name):
    return (
        name.endswith('.py')
        and not name.startswith('__')
        and name != 'game.py'
    )


directory = os.path.dirname(os.path.realpath(__file__))
contents = os.listdir(directory)

games = sorted(name[:-3] for name in contents if is_game(name))

print('''
Memory&Xinxin Games

Here is games list:
''')
for game in games:
    print("    "+game)

print('''
run python -m mxgames.[gamename] to start a game.
for example:
    python -m mxgames.life

have fun with it!
''')
print(mxgames.__copyright__)