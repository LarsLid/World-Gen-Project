import pygame
import random as rd
import math
tile_s = 10
tile_type_colors = {"water" : (0,0,140),
                    "grass" : (0,140,0),
                    "sand"  : (237, 208, 92),
                    "lava"  : (140,0,0)
                    }
def gridGen(grid_size=tuple):
    grid = []
    for i in range(grid_size[0]):
        grid.append([])
        for j in range(grid_size[1]):
            type = "water"
            if rd.randint(0,3)==-1:
                type = "grass"
            grid[i].append(Tile(type, [i, j], tile_type_colors))
    return grid

def drawTiles(screen, grid, camera):
    for row in grid:
        for tile in row:
            tile.draw(screen, camera)

def islandGen(grid, grid_size, island_size):
    global start_gridPos, spiralGrid
    size_remaining = island_size
    start_gridPos = (rd.randint(30,grid_size[0]-30), rd.randint(30,grid_size[1]-30))
    spiralGrid = spiralFromCenter(grid, start_gridPos)
    for i in range(len(spiralGrid)):
        tile = spiralGrid[i]
        roll = rd.randint(0,10)
        touching_grass = sum(1 for x in tile.returnTouching(grid) if x.type == "grass")
        print(touching_grass)
        if (size_remaining/island_size)*15+roll+touching_grass*2 > 15:
            tile.type="grass"
            size_remaining -=1
    return grid

def beachGen(grid):
    for i in range(len(spiralGrid)):
            tile = spiralGrid[i]
            touching_water = sum(1 for x in tile.returnTouching(grid) if x.type == "water")
            if tile.type == "grass" and touching_water >= 3:
                tile.type = "sand"
    return grid




def spiralFromCenter(grid, center):
    cx, cy = center
    rows, cols = len(grid), len(grid[0])
    cells = [(x, y) for x in range(rows) for y in range(cols)]
    cells.sort(key=lambda p: (math.hypot(p[0]-cx, p[1]-cy), math.atan2(p[1]-cy, p[0]-cx)))
    return [grid[x][y] for x, y in cells]



class Tile:
    def __init__(self, type = str, gridPos = list, tile_type_colors = list):
        self.type = type
        self.gridPos = gridPos  # real (i, j) index into the grid list
        self.pos = ((gridPos[0]-50)*tile_s, (gridPos[1]-50)*tile_s)  # centered world position
        tile_s_real = tile_s+5
        self.rect = pygame.Rect(self.pos[0]-tile_s_real//2, self.pos[1]-tile_s_real//2, tile_s_real, tile_s_real)
        self.color = tile_type_colors[self.type]

    def draw(self, screen, camera):
        self.color = tile_type_colors[self.type]
        pygame.draw.rect(screen, self.color, camera.apply_rect(self.rect, screen.get_size()))

    def returnTouching(self, grid):
        touching = []
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                if (i,j) == (0,0):
                    continue
                gi, gj = self.gridPos[0]+i, self.gridPos[1]+j
                if 0 <= gi < len(grid) and 0 <= gj < len(grid[gi]):
                    touching.append(grid[gi][gj])

        return touching


