import pygame


class Camera:
    def __init__(self, x=0, y=0, zoom=1.0, speed=400, zoom_speed=0.1, min_zoom=0.2, max_zoom=5.0):
        self.x = x  # world-space point the camera is centered on
        self.y = y
        self.zoom = zoom
        self.speed = speed  # world units/sec at zoom=1; divided by zoom so screen-space pan speed stays constant
        self.zoom_speed = zoom_speed
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            factor = 1 + event.y * self.zoom_speed
            self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom * factor))

    def update(self, dt, keys):
        move = self.speed * dt / self.zoom
        if keys[pygame.K_w]:
            self.y -= move
        if keys[pygame.K_s]:
            self.y += move
        if keys[pygame.K_a]:
            self.x -= move
        if keys[pygame.K_d]:
            self.x += move

    def world_to_screen(self, pos, screen_size):
        sx = (pos[0] - self.x) * self.zoom + screen_size[0] / 2
        sy = (pos[1] - self.y) * self.zoom + screen_size[1] / 2
        return sx, sy

    def screen_to_world(self, pos, screen_size):
        wx = (pos[0] - screen_size[0] / 2) / self.zoom + self.x
        wy = (pos[1] - screen_size[1] / 2) / self.zoom + self.y
        return wx, wy

    def apply_rect(self, rect, screen_size):
        """World-space rect -> screen-space rect, accounting for pan + zoom."""
        top_left = self.world_to_screen((rect.x, rect.y), screen_size)
        size = (rect.width * self.zoom, rect.height * self.zoom)
        return pygame.Rect(top_left, size)
