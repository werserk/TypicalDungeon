import pygame

pygame.init()
infoObject = pygame.display.Info()
window_size = window_width, window_height = infoObject.current_w,\
                                            int(infoObject.current_h * 0.95)
FPS = 60

size = width, height = 1920, 1080
