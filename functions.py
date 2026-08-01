import pygame
import random as rd
import math
tile_s = 10
tile_type_colors = {"water" : [(0,0,130), (0,0,130), (0,0,140), (0,0,150)],
                    "grass" : [(0,140,0), (0,130, 20)],
                    "sand"  : [(237, 208, 92), (245, 208, 90)],
                    "lava"  : [(140,0,0)]
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
    start_gridPos = (rd.randint(10,grid_size[0]-10), rd.randint(10,grid_size[1]-10))
    spiralGrid = spiralFromCenter(grid, start_gridPos)
    for i in range(len(spiralGrid)):
        tile = spiralGrid[i]
        roll = rd.randint(0,10)
        touching_grass = sum(1 for x in tile.returnTouching(grid) if x.type == "grass")
        if (size_remaining/island_size)*15+roll+touching_grass*2 > 15:
            tile.type="grass"
            size_remaining -=1
        if size_remaining<island_size*0.2: #stops island gen when island "done"
            return grid
    return grid #returns grid incase it wasnt stopped early

def islandGen2(grid, grid_size, island_size):
    global start_gridPos, spiralGrid
    size_remaining = island_size
    start_gridPos = (rd.randint(10,grid_size[0]-10), rd.randint(10,grid_size[1]-10))
    spiralGrid = spiralFromCenter(grid, start_gridPos)
    start_tile = grid[start_gridPos[0]][start_gridPos[1]]
    chosen_tiles = [start_tile]
    while size_remaining > 0:
        possible_tiles = []
        for tile in chosen_tiles:
            possible_tiles.append(tile.returnTouching(grid))
        chosen_tiles = []
        for tile_list in possible_tiles:
            chosen_tile = rd.choice(tile_list)
            chosen_tile.type = "grass"
            chosen_tiles.append(chosen_tile)
            size_remaining -=1
    return grid

            
        
        


def beachGen(grid):
    for j in range(2):
        for i in range(len(spiralGrid)):
                tile = spiralGrid[i]
                touching_grass = sum(1 for x in tile.returnTouching(grid) if x.type == "grass")
                touching_water = sum(1 for x in tile.returnTouching(grid) if x.type == "water")
                touching_sand  = sum(1 for x in tile.returnTouching(grid) if x.type == "sand")
                if tile.type == "grass" and touching_water >= 3  or tile.type == "water" and touching_grass>0 and touching_sand>0:
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
        self.tile_type_colors = tile_type_colors
        self.gridPos = gridPos  # real (i, j) index into the grid list
        self.pos = (gridPos[0]*tile_s, gridPos[1]*tile_s)  # world position; grid's (0,0) corner is world origin
        tile_s_real = tile_s+5
        self.rect = pygame.Rect(self.pos[0]-tile_s_real//2, self.pos[1]-tile_s_real//2, tile_s_real, tile_s_real)
        self.type = type  # goes through the setter below, picking a shade once

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
        self.color = rd.choice(self.tile_type_colors[value])

    def draw(self, screen, camera):
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


