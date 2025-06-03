import pygame


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font,
        callback,
        base_color=(160, 130, 90),
        hover_color=(200, 170, 110),
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, (30, 20, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.base_color
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
