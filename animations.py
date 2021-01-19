import pyganim

ICON_DIR = 'data/creatures/'
ANIMATION_DELAY = 100
STAY_END = [39, 25, 35, 33, 30, 24, 29, 25, 60, 28, 28, 28, 22, 30, 30]
ATK_END = [97, 46, 73, 85, 52, 55, 47, 43, 94, 46, 59, 52, 46, 50, 47]


def load_animations(num):
    dirs_animation_1_stay = [('{ICON_DIR}{creature}/anim/{i}.png'.format(
        ICON_DIR=ICON_DIR, creature=num, i=i), ANIMATION_DELAY) for i in
        range(0, STAY_END[num] + 1)]
    dirs_animation_1_atk = [
        ('{ICON_DIR}{creature}/anim/{i}.png'.format(
            ICON_DIR=ICON_DIR, creature=num, i=i), ANIMATION_DELAY) for i in
        range(STAY_END[num] + 1, ATK_END[num]+1)]
    animation_1_stay = pyganim.PygAnimation(dirs_animation_1_stay)
    animation_1_atk = pyganim.PygAnimation(dirs_animation_1_atk, loop=False)
    return animation_1_stay, animation_1_atk
