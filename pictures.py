from helpers import load_image
import os

BACKGROUNDS = {'desert': 'Background_250.png',
               'jungle': 'Background_239.png',
               'plain': 'Background_178.png',
               'crimson': 'Background_230.png',
               'lake': 'Background_251.png',
               'dungeon': ['bg1.png', 'bg3.png', 'bg4.png']}
for key in BACKGROUNDS.keys():
    if isinstance(BACKGROUNDS[key], str):
        BACKGROUNDS[key] = load_image('data/backgrounds/' + BACKGROUNDS[key])
    else:
        pics = []
        for i in BACKGROUNDS[key]:
            pics.append(load_image('data/backgrounds/' + i))
        BACKGROUNDS[key] = pics

EARTH = {'desert': 'Background_218.png',
         'jungle': 'Background_17.png',
         'plain': ['Background_224.png', 'Background_224.png',
                   'Background_224.png'],
         'crimson': ['Background_256.png', 'Background_257.png']}

LINE = load_image('data/UI/line.png')
TEXT_FRAME = load_image('data/UI/Chat.png')

CLOUDS = [load_image('data/clouds/' + name)
          for name in os.listdir('data/clouds/')]

EMPTY = load_image('data/empty.png')
ARROW = load_image('data/pointer.png')
IN_DUNGEON = load_image('data/go_in_dungeon/MapBG4.png')
CREATURES = load_image('data/go_in_dungeon/creatures.png')
SHOP = load_image('data/go_in_dungeon/shop.png')
CRYSTAL = load_image('data/crystal.png')
IN_SHOP = load_image('data/go_in_dungeon/in_shop.jpg')
CARD = load_image('data/card.png')
