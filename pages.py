from objects import *
import sys
import pygame
from sounds import *
from texts import *
from pictures import *
import time

background_music = Music(BACKGROUND_MUSIC)
sounder = Sounder()
fullscreener = FullScreener()
blackouter = Blackouter()


class PlainBackground:
    def __init__(self):
        self.clouds = pygame.sprite.Group()
        self.background = BACKGROUNDS['lake']
        self.pre_time = 0

        self.create_cloud(self.clouds, x=width // 2 + 100)
        self.create_cloud(self.clouds, x=width // 2 + -150)

    def create_cloud(self, group, x=None, y=None):
        self.pre_time = time.time()
        if not x:
            x = random.choice([0, width])
        if not y:
            y = random.randrange(20, 200)
        speed = random.random() * 3
        flag = 'topright'
        if x == width:
            speed *= -1
            flag = 'topleft'
        cloud = Cloud(random.choice(CLOUDS), x, y, flag, speed)
        group.add(cloud)

    def update(self):
        if time.time() - self.pre_time > 7 and len(self.clouds) < 4:
            self.create_cloud(self.clouds)
        self.clouds.update()

    def draw(self, surface):
        surface.fill((150, 150, 255))
        if self.background.get_size() != surface.get_size():
            self.background = resize(self.background, surface.get_size())
        surface.blit(self.background, (0, 100))
        self.clouds.draw(surface)


class MainPage:
    def __init__(self):
        self.current_page = 0
        self.buttons = pygame.sprite.Group()

        self.buttons.add(Button((width // 2, height // 2 - 62, None, None),
                                flag='center', text='Play', image=EMPTY,
                                func=self.play))
        self.buttons.add(Button((width // 2, height // 2, None, None),
                                flag='center', text='Options', image=EMPTY,
                                func=self.open_options))
        self.buttons.add(
            Button((width // 2, height // 2 + 62, None, None),
                   flag='center', text='Exit', image=EMPTY, func=sys.exit))

    def draw(self, surface):
        self.buttons.draw(surface)

    def update(self, events):
        self.buttons.update(events)
        if self.current_page == 2:
            return {'page': OptionsPage()}
        elif self.current_page == 1:
            if FIRST_TIME:
                return {'page': HelloPage()}
            else:
                return {'page': PlayingPage()}

    def open_options(self):
        self.current_page = 2
        sounder.play(CLICK_SOUND)

    def play(self):
        self.current_page = 1
        sounder.play(CLICK_SOUND)


class OptionsPage:
    def __init__(self):
        self.current_page = 0
        self.buttons = pygame.sprite.Group()

        self.btn_screen = Button((width // 2, height // 2 - 62, None, None),
                                 flag='center',
                                 text='Full Screen/In Window',
                                 image=EMPTY,
                                 func=self.full_screen)

        self.btn_music = Button((width // 2, height // 2, None, None),
                                flag='center',
                                text='Music On/Off',
                                image=EMPTY,
                                func=self.music)

        self.btn_sound = Button((width // 2, height // 2 + 62, None, None),
                                flag='center',
                                text='Sounds On/Off',
                                image=EMPTY,
                                func=self.sound)

        self.buttons.add(self.btn_screen)
        self.buttons.add(self.btn_sound)
        self.buttons.add(self.btn_music)
        self.buttons.add(
            Button((width // 2, height // 2 + 124, None, None),
                   flag='center', text='Back', image=EMPTY,
                   func=self.back))

    def full_screen(self):
        fullscreener.switch()
        fullscreener.apply()
        sounder.play(CLICK_SOUND)

    def music(self):
        background_music.switch()
        background_music.play()
        sounder.play(CLICK_SOUND)

    def sound(self):
        sounder.switch()
        sounder.play(CLICK_SOUND)

    def back(self):
        self.current_page = -1
        sounder.play(CLICK_SOUND)

    def update(self, events):
        self.buttons.update(events)
        if self.current_page == -1:
            return {'page': MainPage()}

    def draw(self, surface):
        self.buttons.draw(surface)


class HelloPage:
    def __init__(self):
        self.current_page = 0
        self.all_sprites = pygame.sprite.Group()

        self.frame = EasySprite(resize(TEXT_FRAME, (1000, 800)),
                                width // 2, height // 2, flag='center')
        self.all_sprites.add(self.frame)

        for i, line in enumerate(HELLO_TEXT):
            text = Text(line, width // 2, int((i + 3.5) * 62), flag='center')
            self.all_sprites.add(text)

        self.btn_ok = Button((width // 2, height - 100, None, None),
                             flag='center', func=self.ok, text='Ok',
                             image=EMPTY)
        self.all_sprites.add(self.btn_ok)

    def update(self, events):
        self.all_sprites.update(events)
        if self.current_page == 1:
            return {'page': PlayingPage()}

    def draw(self, surface):
        self.all_sprites.draw(surface)

    def ok(self):
        sounder.play(CLICK_SOUND)
        self.current_page = 1
        with open('data/info.txt') as f:
            lines = f.read().split('\n')
        with open('data/info.txt', mode='w') as f:
            lines[0] = lines[0][:-1] + '0'
            f.write('\n'.join(lines))


class InfoPage:
    def __init__(self):
        self.current_page = 0
        self.all_sprites = pygame.sprite.Group()
        self.frame = EasySprite(resize(TEXT_FRAME, (1400, 800)), width // 2,
                                height // 2, flag='center')
        self.all_sprites.add(self.frame)
        for i, line in enumerate(INFO_TEXT):
            text = Text(line, width // 2 - 650, int((i + 4) * 40), size=25)
            self.all_sprites.add(text)
        self.btn_back = Button((width // 2, height - 50, None, None),
                               flag='center', func=self.back, text='Back',
                               image=EMPTY)
        self.all_sprites.add(self.btn_back)

    def update(self, events):
        self.all_sprites.update(events)
        if self.current_page == -1:
            return {'page': PlayingPage()}

    def draw(self, surface):
        self.all_sprites.draw(surface)

    def back(self):
        sounder.play(CLICK_SOUND)
        self.current_page = -1


class PlayingPage:
    def __init__(self):
        self.current_page = 0
        self.all_sprites = pygame.sprite.Group()
        self.money = get_money()

        self.btn_how_to_play = Button((10, 10, None, None),
                                      text='HOW TO PLAY',
                                      text_size=30,
                                      func=self.how_to_pay)
        self.btn_back = Button((10, height - 10, None, None),
                               text='Back',
                               text_size=30,
                               func=self.back,
                               flag='leftbottom')
        self.btn_go_in_dungeon = Button((width // 2, height // 2, 400, 230),
                                        image=IN_DUNGEON,
                                        text='DUNGEON',
                                        text_size=30,
                                        func=self.go_in_dungeon,
                                        flag='center')
        self.btn_creatures = Button((width // 2 + 500, height // 2, 360, 200),
                                    image=CREATURES,
                                    text='CREATURES',
                                    text_size=30,
                                    func=self.creatures,
                                    flag='center')
        self.btn_shop = Button((width // 2 - 500, height // 2, 360, 200),
                               image=SHOP,
                               text='SHOP',
                               text_size=30,
                               func=self.go_in_shop,
                               flag='center')
        self.money = Text('Money:{}'.format(self.money), width - 10, 10,
                          flag='righttop',
                          color=(255, 255, 0))

        self.all_sprites.add(self.btn_how_to_play)
        self.all_sprites.add(self.btn_back)
        self.all_sprites.add(self.btn_go_in_dungeon)
        self.all_sprites.add(self.btn_creatures)
        self.all_sprites.add(self.btn_shop)
        self.all_sprites.add(self.money)

    def update(self, events):
        if self.current_page == -1:
            return {'page': MainPage(), 'bg': PlainBackground()}
        if self.current_page == 1:
            return {'page': InfoPage(), 'bg': PlainBackground()}

        if self.current_page and blackouter.is_ready():
            if self.current_page == 2:
                return {'page': ShopPage(), 'bg': IN_SHOP.copy()}
            if self.current_page == 3:
                return {'page': CreaturesPage(),
                        'bg': BACKGROUNDS['dungeon'][0].copy()}
            if self.current_page == 4:
                return {'page': BattlePage(),
                        'bg': BACKGROUNDS['dungeon'][random.randint(0, 2)]}
        elif not self.current_page and blackouter.is_ok():
            self.all_sprites.update(events)

    def draw(self, surface):
        if self.current_page >= 2:
            blackouter.make_blackout(surface)

        if self.current_page == 0:
            blackouter.remove_blackout(surface)

        self.all_sprites.draw(surface)

    def how_to_pay(self):
        sounder.play(CLICK_SOUND)
        self.current_page = 1

    def go_in_shop(self):
        sounder.play(CLICK_SOUND)
        self.current_page = 2

    def go_in_dungeon(self):
        sounder.play(CLICK_SOUND)
        self.current_page = 4

    def creatures(self):
        sounder.play(CLICK_SOUND)
        self.current_page = 3

    def back(self):
        sounder.play(CLICK_SOUND)
        self.current_page = -1


class ShopPage:
    def __init__(self):
        self.current_page = 0
        self.all_sprites = pygame.sprite.Group()
        self.money = get_money()
        self.creature = None
        self.flashed = False

        self.btn_back = Button((10, height - 10, None, None),
                               text='Back',
                               text_size=30,
                               func=self.back,
                               flag='leftbottom',
                               text_color=(255, 255, 255))
        self.btn_buy = Button((width // 2, height // 2 + 300, 500, 90),
                              text='Buy',
                              text_size=50,
                              func=self.buy,
                              flag='center',
                              image=LINE)
        self.txt_money = Text('Money:{}'.format(self.money), width - 10, 10,
                              flag='righttop',
                              color=(255, 255, 0))
        self.btn_ok = Button((width // 2, height // 2 + 300, 500, 90),
                             text='Ok',
                             text_size=50,
                             func=self.ok,
                             flag='center')

        self.all_sprites.add(self.btn_back)
        self.all_sprites.add(self.btn_buy)
        self.all_sprites.add(self.txt_money)

    def back(self):
        sounder.play(CLICK_SOUND)
        self.current_page = -1

    def buy(self):
        sounder.play(CLICK_SOUND)
        money = get_money()
        if money >= 1000:

            prize = random.choices(range(13), weights=[0.1] + [0.5] * 12)[0]
            level = random.choices(range(1, 4), weights=[0.75, 0.5, 0.25])[0]
            with open('data/info.txt') as f:
                lines = f.read().split('\n')
            with open('data/info.txt', mode='w') as f:
                lines[1] = lines[1].split(':')[0] + ':' + str(money - 1000)
                _creatures_text, creatures = lines[2].split(':')
                creatures = eval(creatures)
                creatures.append((prize, level))
                res = str(creatures)
                if res == 'None':
                    res = '[]'
                lines[2] = lines[2].split(':')[0] + ':' + res
                f.write('\n'.join(lines))
            self.creature = CreatureCard(width // 2, height // 2 - 100,
                                         flag='center', number=prize,
                                         lvl=level)
            self.btn_back.kill()
            self.btn_buy.kill()
            self.txt_money.kill()
            self.all_sprites.add(self.btn_ok)
            self.all_sprites.add(self.creature)
            self.flashed = True
            self.money = get_money()

    def update(self, events):
        if self.current_page and blackouter.is_ready():
            if self.current_page == -1:
                return {'page': PlayingPage(), 'bg': PlainBackground()}
        elif not self.current_page and blackouter.is_ok():
            self.all_sprites.update(events)

    def draw(self, surface):
        if self.current_page == 0:
            blackouter.remove_blackout(surface)

        if self.current_page == -1:
            blackouter.make_blackout(surface)

        if self.flashed:
            surface.fill((255, 255, 255))
        self.all_sprites.draw(surface)

    def ok(self):
        self.txt_money = Text('Money:{}'.format(self.money), width - 10, 10,
                              flag='righttop', color=(255, 255, 0))
        self.btn_ok.kill()
        self.creature.kill()

        self.flashed = False

        self.all_sprites.add(self.btn_buy)
        self.all_sprites.add(self.btn_back)
        self.all_sprites.add(self.txt_money)


class CreaturesPage:
    def __init__(self):
        self.current_page = 0
        self.creatures = []
        self.all_sprites = pygame.sprite.Group()
        self.page = 1
        self.count_of_buttons = 0

        self.btn_back = Button((10, height - 10, None, None),
                               text='Back',
                               text_size=30,
                               func=self.back,
                               flag='leftbottom',
                               text_color=(255, 255, 255))

        self.btn_right = Button((width - 60, height // 2, None, None),
                                text='>',
                                text_size=50,
                                func=self.right,
                                flag='center',
                                text_color=(255, 255, 255))

        self.btn_left = Button((60, height // 2, None, None),
                               text='<',
                               text_size=50,
                               func=self.left,
                               flag='center',
                               text_color=(255, 255, 255))

        self.all_sprites.add(self.btn_back)
        self.all_sprites.add(self.btn_left)
        self.all_sprites.add(self.btn_right)

        with open('data/info.txt') as f:
            lines = f.read().split('\n')
            _creatures_text, creatures = lines[2].split(':')
            creatures = eval(creatures)
            self.all_pages = (len(creatures) + 4) // 5
            for i, info in enumerate(creatures):
                num, lvl = info
                card = CreatureCard((i % 5 + 1) * 300 - 100,
                                    height // 3, None, num, lvl)
                self.creatures.append(card)

    def back(self):
        sounder.play(CLICK_SOUND)
        self.current_page = -1

    def right(self):
        sounder.play(CLICK_SOUND)
        if self.page < self.all_pages:
            self.page += 1

    def left(self):
        sounder.play(CLICK_SOUND)
        if self.page > 1:
            self.page -= 1

    def update(self, events):
        if self.current_page == -1 and blackouter.is_ready():
            return {'page': PlayingPage(), 'bg': PlainBackground()}
        self.all_sprites.update(events)

    def draw(self, surface):
        creatures = pygame.sprite.Group()

        if self.current_page == 0:
            blackouter.remove_blackout(surface)
        elif self.current_page == -1:
            blackouter.make_blackout(surface)

        if self.creatures:
            for i, creature in enumerate(
                    self.creatures[5 * (self.page - 1): 5 * self.page]):
                creatures.add(Button(creature.rect, image=creature.image))
        self.all_sprites.draw(surface)
        creatures.draw(surface)


class BattlePage:
    def __init__(self):
        self.start_time = time.time()
        self.current_page = 0
        self.creatures = []
        self.all_sprites = pygame.sprite.Group()

        coords_my_team = [(width // 2 - 400, height // 2 + 150),
                          (width // 2 - 100, height // 2 + 300),
                          (width // 2 - 400, height // 2 + 450)]

        with open('data/info.txt') as f:
            lines = f.read().split('\n')
            _creatures_text, creatures = lines[2].split(':')
            creatures = eval(creatures)
            random.shuffle(creatures)
            creatures = creatures[:3]
            for i, info in enumerate(creatures):
                num, lvl = info
                card = CreatureCard(coords_my_team[i][0] - 300,
                                    coords_my_team[i][1], 'center', num, lvl)
                self.creatures.append(Creature(card, my=True))

        self.my_team = self.creatures
        self.opponents_team = []
        self.can_attack_creatures = []
        self.btn_back = Button((10, height - 10, None, None),
                               text='Exit from dungeon',
                               text_size=30,
                               func=self.back,
                               flag='leftbottom',
                               text_color=(255, 255, 255))
        self.text_me = Text('Me', 10, 10, color=(255, 255, 255))
        self.text_opponent = Text('Opponent', width - 10, 10,
                                  color=(255, 255, 255),
                                  flag='righttop')
        self.floor = 1

        self.generate_opponents()

        self.btns = pygame.sprite.Group()
        self.btns.add(self.btn_back)
        self.btns.add(self.text_me)
        self.btns.add(self.text_opponent)
        self.attacker = None

        self.all_sprites = pygame.sprite.Group()

        for creature in self.my_team:
            self.all_sprites.add(creature)
        for creature in self.opponents_team:
            self.all_sprites.add(creature)

    def update(self, events):
        if self.current_page == -1:
            return {'page': PlayingPage(), 'bg': PlainBackground()}

        self.btns.update(events)

        creatures_c = self.all_sprites.sprites()

        if time.time() - self.start_time < 2:
            return

        for creature in self.my_team:
            if creature.hp <= 0:
                self.my_team.remove(creature)

        for creature in self.opponents_team:
            if creature.hp <= 0:
                self.opponents_team.remove(creature)

        if not self.opponents_team or not self.my_team:
            return {'page': PlayingPage(), 'bg': PlainBackground()}

        if not self.can_attack_creatures and not self.attacker:
            attacker = max(creatures_c, key=lambda x: x.powers)
            power_up = (1 - attacker.powers) / attacker.speed
            self.all_sprites.update(power_up)

        if not self.attacker:
            if self.can_attack_creatures:
                self.attacker = self.can_attack_creatures.pop()
                if self.attacker.my:
                    self.attacker.attack(min(self.opponents_team,
                                             key=lambda x: x.hp))
                else:
                    self.attacker.attack(min(self.my_team,
                                             key=lambda x: x.hp))
                self.atk_time = time.time()
        else:
            f = time.time() - self.atk_time > len(
                self.attacker.anim_atk._images) * 0.1
            if self.attacker.anim_atk.isFinished() or f:
                self.attacker.stay()
                self.attacker = None

        self.can_attack_creatures = list(filter(
            lambda x: x.can_attack or x.powers >= 1, creatures_c))

    def generate_opponents(self):
        coords_opponents_team = [(width // 2 + 400, height // 2 + 150),
                                 (width // 2 + 100, height // 2 + 300),
                                 (width // 2 + 400, height // 2 + 450)]
        for i in range(random.randint(1, 3)):
            prize = random.randint(0, 13)

            with open('data/info.txt') as f:
                lines = f.read().split('\n')
                creatures = lines[2].split(':')[1]
                creatures = eval(creatures)
                creatures.append((prize, 1))
                creature = CreatureCard(coords_opponents_team[i][0] + 300,
                                        coords_opponents_team[i][1], flag='center',
                                        number=prize,
                                        lvl=random.randint(
                                            1 * self.floor, 3 * self.floor))
                creature = Creature(creature)
            self.opponents_team.append(creature)

    def back(self):
        sounder.play(CLICK_SOUND)
        self.current_page = -1

    def draw(self, surface):
        if self.current_page == 0:
            blackouter.remove_blackout(surface)
        for sprite in self.all_sprites.sprites():
            image, rect = sprite.image, sprite.rect
            x, y, w, h, = rect
            image.blit(surface, (x - w // 2, y - h // 2))

            health_bar = pygame.Surface((120, 6))
            health_bar.fill((255, 255, 255))
            health = pygame.Surface((int(120 * sprite.hp / sprite.card.hp), 6))
            health.fill((255, 30, 30))
            health_bar.blit(health, (0, 0))

            speed_bar = pygame.Surface((120, 6))
            speed_bar.fill((255, 255, 255))
            speed = pygame.Surface((int(120 * sprite.powers), 6))
            speed.fill((30, 255, 30))
            speed_bar.blit(speed, (0, 0))

            surface.blit(health_bar, (x - 65, y + h // 3 + 30))
            surface.blit(speed_bar, (x - 65, y + h // 3 + 36))
        self.btns.draw(surface)
