import pygame
import os
import sys


def cut_by_net(image, size):
    num_x, num_y = size
    pictures = []

    side_y = image.get_height() // num_y
    side_x = image.get_width() // num_x

    for y in range(num_y):
        for x in range(num_x):
            cropped = pygame.Surface((side_x, side_y))
            cropped.blit(image, (0, 0),
                         pygame.rect.Rect(side_x * x, side_y * y, side_x * (x + 1), side_y * (y + 1)))
            pictures.append(cropped)

    return pictures


def resize(image, size=None, scaling_size=1):
    if size:
        image = pygame.transform.scale(image, size)
    image = pygame.transform.scale(image,
                                   (int(image.get_width() * scaling_size),
                                    int(image.get_height() * scaling_size)))
    return image


def rotate_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def flip_vertical(image):
    return pygame.transform.flip(image, False, True)


def flip_horizontal(image):
    return pygame.transform.flip(image, True, False)


def load_image(full_name, color_key=None):
    if not os.path.isfile(full_name):
        print(f'File {full_name} not found')
        sys.exit()
    image = pygame.image.load(full_name)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image
