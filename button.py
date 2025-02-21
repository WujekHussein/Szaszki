from copy import deepcopy

import pygame
import copy


class Button:
    def __init__(self, x, y, width, height, text, font, action = None, border_width=3, color = "white", text_color = "black",  border_color="black"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = font.render(text, True, text_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.border_color = border_color
        self.border_width = border_width
        self.action = action
        self.is_active = True


    def draw(self, surface):
        # Draw border (bigger rectangle)
        pygame.draw.rect(surface, self.border_color, self.rect.inflate(self.border_width * 2, self.border_width * 2))

        # Draw button background
        pygame.draw.rect(surface, self.color, self.rect)

        # Draw text
        surface.blit(self.text, self.text_rect)

    def is_hovered(self):
        """Returns True if mouse is over the button"""
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def check_pushdown(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
    def check_release(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            return self.rect.collidepoint(event.pos)
    def act(self):
        if self.action:
            self.action(self)



class TileButton(Button):
    def __init__(self, x, y, width, height, text, font, action, board_coords, border_width=3, color = "white", text_color = "black",  border_color="black"):
        super().__init__(x, y, width, height, text, font, action, border_width, color, text_color,  border_color)
        self.board_coords = board_coords

    def draw(self, surface):

        # Draw button background
        pygame.draw.rect(surface, self.color, self.rect)

        # Draw text
        surface.blit(self.text, self.text_rect)

    def __str__(self):
        x, y = self.board_coords
        return chr(y+97)+chr(x+49)