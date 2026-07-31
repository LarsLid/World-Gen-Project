import pygame
import sys
import math

from camera import Camera
from functions import *

pygame.init()

WIDTH, HEIGHT = 1200, 700
cx, cy = WIDTH//2, HEIGHT//2
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("World Gen")

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
camera = Camera()



grid = gridGen()





running = True
while running:
    dt = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            cx, cy = WIDTH // 2, HEIGHT // 2
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        camera.handle_event(event)

    camera.update(dt, pygame.key.get_pressed())

    #DRAWING BELOW
    screen.fill((0,250,0))

    drawTiles(screen, grid, camera)



    pygame.display.flip()

pygame.quit()
sys.exit()