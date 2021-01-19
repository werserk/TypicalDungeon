from pages import *


def main():
    # Активация pygame
    pygame.init()

    # Базовая настройка
    window = pygame.display.set_mode(window_size,
                                     pygame.RESIZABLE | pygame.DOUBLEBUF)
    pygame.display.set_caption('Typical Dungeon')
    pygame.display.set_icon(load_image('data/icon.png'))
    pygame.mouse.set_visible(False)

    # Для управления временем
    clock = pygame.time.Clock()

    # Поле, на котором будем всё рисовать
    screen = pygame.Surface(size)

    # Активная страница
    current_page = MainPage()

    # Фон
    background_page = PlainBackground()

    # Состояние игры
    running = True

    # Основной цикл
    while running:
        events = pygame.event.get()
        types = []
        for event in events:
            types.append(event.type)
            if types[-1] == pygame.QUIT:
                running = False

        # Обновление
        callback = current_page.update(types)

        if callback:
            if 'page' in callback.keys():
                current_page = callback['page']

            if 'bg' in callback.keys():
                background_page = callback['bg']

        if isinstance(background_page, PlainBackground):
            background_page.update()
            background_page.draw(screen)
        else:
            if background_page.get_size() != screen.get_size():
                background_page = resize(background_page, screen.get_size())
            screen.blit(background_page, (0, 0))

        # Отрисовка на экране моего размера
        current_page.draw(screen)

        # Отрисовка на экране пользовательского размера
        scaling_size = min(window.get_height() / height,
                           window.get_width() / width)
        _screen = resize(screen, scaling_size=scaling_size)
        window.fill((0, 0, 0))
        window.blit(_screen,
                    (max((window.get_width() - _screen.get_width()) // 2, 0),
                     max((window.get_height() - _screen.get_height()) // 2,
                         0)))

        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            window.blit(resize(ARROW, scaling_size=(scaling_size - 0.05)),
                        (x, y))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
