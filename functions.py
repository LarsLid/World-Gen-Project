import pygame
import random as rd
tile_s = 10
tile_type_colors = {"water" : (0,0,140),
                    "grass" : (0,140,0)
                    }
def gridGen():
    grid = []
    for i in range(100):
        grid.append([])
        for j in range(100):
            type = "water"
            if rd.randint(0,3)==0:
                type = "grass"
            grid[i].append(Tile(type, (-200+i*tile_s, -200+j*tile_s), tile_type_colors))
    return grid

def drawTiles(screen, grid, camera):
    for row in grid:
        for tile in row:
            tile.draw(screen, camera)
        



class Tile:
    def __init__(self, type = str, pos = tuple, tile_type_colors = list):
        self.type = type
        self.pos = pos
        tile_s_real = tile_s+5
        self.rect = pygame.Rect(pos[0]-tile_s_real//2, pos[1]-tile_s_real//2, tile_s_real, tile_s_real)
        self.color = tile_type_colors[self.type]

    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.color, camera.apply_rect(self.rect, screen.get_size()))

