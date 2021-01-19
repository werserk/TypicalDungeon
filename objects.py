import pygame
from pictures import *
import random
from settings import *
from helpers import *
from sounds import *
from animations import *
import pyganim


class Blackouter:
    def __init__(self):
        self.value = 255

    def make_blackout(self, surface: pygame.Surface):
        surface.set_alpha(self.value)
        if self.value > -15:
            self.value -= 25

    def remove_blackout(self, surface: pygame.Surface):
        surface.set_alpha(self.value)
        if self.value < 255:
            self.value += 25

    def is_ready(self):
        return self.value < 0

    def is_ok(self):
        return self.value >= 255


class EasySprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int, flag=None):
        super().__init__()
        self.set_image(image)
        self.set_coords(x, y, flag)

    def set_coords(self, x, y, flag=None):
        if flag is None:
            self.rect.x = x
            self.rect.y = y
            return
        if flag == 'center':
            self.rect.centerx = x
            self.rect.centery = y
        else:
            if 'bottom' in flag:
                self.rect.bottom = y
            elif 'top' in flag:
                self.rect.top = y
            if 'right' in flag:
                self.rect.right = x
            elif 'left' in flag:
                self.rect.left = x

    def set_image(self, image):
        self.image = image
        if isinstance(self.image, pyganim.PygAnimation):
            self.rect = self.image.getRect()
        else:
            self.rect = image.get_rect()


class FullScreener:
    def __init__(self):
        self.fullscreen = False

    def switch(self):
        self.fullscreen = not self.fullscreen

    def apply(self):
        if self.fullscreen:
            pygame.display.set_mode(pygame.display.get_surface().get_size(), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        else:
            pygame.display.set_mode(pygame.display.get_surface().get_size(), pygame.RESIZABLE | pygame.DOUBLEBUF)


class Sounder:
    def __init__(self):
        self.can_play = True

    def play(self, sound):
        if self.can_play:
            sound.play()

    def switch(self):
        self.can_play = not self.can_play


class Music:
    def __init__(self, music):
        self.can_play = True
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(20 / 100)

    def play(self):
        if self.can_play:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def switch(self):
        self.can_play = not self.can_play


class Text(EasySprite):
    def __init__(self, text, x=0, y=0, flag=None, size=30, color=(0, 0, 0), image=None):
        self.f = pygame.font.Font('data/Segoe Print.ttf', size)
        self.text = self.f.render(text, False, color)
        if image:
            image = resize(image, self.text.get_size())
            image.blit(self.text, (0, 0))
            self.image = image.copy()
        else:
            self.image = self.text
        self.rect = self.image.get_rect()
        super().__init__(self.image, x, y, flag)

    def inscribe_in_rect(self, rect: pygame.rect.Rect):
        self.image = resize(EMPTY, rect.size)
        self.image.blit(self.text, (rect.width // 2 - self.text.get_width() // 2,
                                    rect.height // 2 - self.text.get_height() // 2))


class Button(EasySprite):
    def __init__(self, rect, type_of_im=None, flag=None, image=None, text=None, func=None,
                 text_color=(0, 0, 0), text_size=30, args=None):
        x, y, w, h = rect
        self.text_size = text_size
        self.func = func
        self.text_color = text_color
        self.args = args

        # Background кнопки
        if type_of_im == 'empty' or image is None:
            image = EMPTY
        self.image = image.copy()
        self.background = self.image.copy()  # Дальше будет использоваться, как чистая кнопка

        if not (w is None and h is None):  # Если есть размеры, то вписать картинку в них
            self.image = resize(self.image, (w, h))
            self.background = resize(self.background, (w, h))

        # Текст на кнопке
        self.text = text
        if self.text:
            self.set_text(self.text, text_color, text_size, w is None and h is None)

        super().__init__(self.image, x, y, flag)

    def set_text(self, text, text_color, size=30, resize_image=False):
        if resize_image:
            self.image = None
        if text:
            _text = Text(text, color=text_color, size=size)
            if self.image:
                _text.inscribe_in_rect(self.image.get_rect())
            else:
                self.background = resize(self.background,
                                         (int(_text.text.get_width() * 1.1), _text.text.get_height() + 8))

            self.image = self.background.copy()
            self.image.blit(_text.image, (0, 0))

    def set_func(self, func):
        self.func = func

    def update(self, events):
        mouse = pygame.mouse.get_pos()
        x, y = mouse
        scaling_size = min(pygame.display.get_surface().get_height() / height,
                           pygame.display.get_surface().get_width() / width)
        delta_x = pygame.display.get_surface().get_width() - width * scaling_size
        delta_y = pygame.display.get_surface().get_height() - height * scaling_size
        x -= self.rect.x * scaling_size + delta_x // 2
        y -= self.rect.y * scaling_size + delta_y // 2
        if 0 <= x <= self.rect.w * scaling_size and 0 <= y <= self.rect.h * scaling_size:
            self.set_text(self.text, text_color=(200, 0, 200), size=self.text_size + 3)
            if pygame.mouse.get_pressed()[0] and pygame.MOUSEBUTTONDOWN in events:
                if self.func:
                    if self.args:
                        self.func(*self.args)
                    else:
                        self.func()
        else:
            self.set_text(self.text, text_color=self.text_color, size=self.text_size)


class Cloud(EasySprite):
    def __init__(self, image: pygame.Surface, x: int, y: int, flag=None, speed_x=0):
        self.speed_x = speed_x
        self.x = x
        if flag == 'topright':
            self.x -= image.get_width()
        super().__init__(image, x, y, flag)

    def update(self):
        self.x += self.speed_x
        self.rect.x = round(self.x)
        if self.rect.x < 0 - self.rect.w or self.rect.x > width:
            self.kill()


class CreatureCard(EasySprite):
    def __init__(self, x, y, flag, number, lvl):
        self.lvl = lvl
        self.number = number
        self.exp = (lvl - 1) * 1000
        lvl = min(lvl, 50)
        lvl -= 1
        folder_path = 'data/creatures/{}/'.format(number)

        with open(folder_path + 'info.txt') as f:
            text = f.read().split('\n')

        name = text[0].split(':')[1]
        hp = int(text[1].split(':')[1])
        dmg = int(text[2].split(':')[1])
        speed = int(text[3].split(':')[1])

        self.name = name
        self.hp = int(hp * 1.05 ** lvl)
        self.dmg = int(dmg * 1.05 ** lvl)
        self.speed = speed

        card = CARD.copy()
        text_color = pygame.Color('#371902')

        all_sprites = pygame.sprite.Group()
        self.pic = EasySprite(resize(load_image(folder_path + 'anim/0.png'), (250, 250)), card.get_width() // 2, 160,
                              flag='center')

        all_sprites.add(self.pic)
        all_sprites.add(Text(self.name, card.get_width() // 2, 20, flag='center', color=text_color, size=25))
        all_sprites.add(Text('lvl ' + str(lvl + 1), card.get_width() // 2, 60, flag='center', size=18,
                             color=text_color))
        all_sprites.add(Text(str(self.hp), card.get_width() - 20, card.get_height() // 2 + 95,
                             color=text_color, size=25, flag='righttop'))
        all_sprites.add(Text(str(self.dmg), card.get_width() - 20, card.get_height() // 2 + 120,
                             color=text_color, size=25, flag='righttop'))
        all_sprites.add(Text(str(self.speed), card.get_width() - 20, card.get_height() // 2 + 140,
                             color=text_color, size=25, flag='righttop'))

        all_sprites.draw(card)

        super().__init__(card, x, y, flag)


class Creature(EasySprite):
    def __init__(self, card: CreatureCard, my=False):
        self.start_x = card.rect.x
        self.start_y = card.rect.y
        self.my = my
        self.number = card.number
        self.card = card
        self.anim_stay, self.anim_atk = load_animations(self.number)
        if not my:
            self.anim_stay.flip(True, False)
            self.anim_atk.flip(True, False)
        self.anim_stay.play()
        super().__init__(self.anim_stay, self.start_x, self.start_y, None)
        self.speed = card.speed / 100
        self.dmg = card.dmg
        self.hp = card.hp
        self.powers = self.speed
        self.can_attack = False

    def attack(self, creature):
        if creature.my != self.my:
            dmg = self.dmg
            if random.random() < 0.1:
                dmg *= 5
            creature.deal_damage(dmg)
            if creature.hp <= 0:
                self.card.exp += 100
            self.anim_atk.play()
            self.anim_stay.togglePause()
            self.set_image(self.anim_atk)
            self.rect.x = creature.rect.x + 100 - 200 * self.my
            self.rect.y = creature.rect.y
            self.can_attack = False
            self.powers = 0

    def stay(self):
        self.anim_atk.stop()
        self.anim_stay.togglePause()
        self.set_image(self.anim_stay)
        self.rect.x = self.start_x
        self.rect.y = self.start_y

    def deal_damage(self, dmg):
        if random.random() < 0.1:
            dmg = 0
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()
            if not self.my:
                with open('data/info.txt') as f:
                    lines = f.read().split('\n')
                with open('data/info.txt', mode='w') as f:
                    t, money = lines[1].split(':')
                    money = int(money)
                    lines[1] = t + ':' + str(money + 100)
                    f.write('\n'.join(lines))

    def update(self, delta):
        self.powers += delta * self.speed
        if self.powers >= 1:
            self.can_attack = True
            self.powers = 1
