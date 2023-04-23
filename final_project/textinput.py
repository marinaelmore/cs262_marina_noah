#!/usr/bin/env python
""" pg.examples.textinput
A little "console" where you can write in text.
Shows how to use the TEXTEDITING and TEXTINPUT events.
"""
import sys
import os

import pygame
import pygame as pg
import pygame.freetype as freetype
from config import *

# This environment variable is important
# If not added the candidate list will not show
os.environ["SDL_IME_SHOW_UI"] = "1"

class TextInput:
    """
    A simple TextInput class that allows you to receive inputs in pygame.
    """

    def __init__(
        self, prompt: str, pos, screen_dimensions, print_event: bool, text_color="white"
    ) -> None:
        self.prompt = prompt
        self.print_event = print_event
        # position of chatlist and chatbox
        self.CHAT_BOX_POS = pg.Rect(pos, (screen_dimensions[1], 40))

        self._ime_editing = False
        self._ime_text = ""
        self._ime_text_pos = 0
        self._ime_editing_text = ""
        self._ime_editing_pos = 0

        # Freetype
        self.text_color = BLUE
        self.font = freetype.SysFont(None, 20)

    def update(self, events) -> None:
        """
        Updates the text input widget
        """
        for event in events:
            if event.type == pg.KEYDOWN:
                if self.print_event:
                    print(event)

                if self._ime_editing:
                    if len(self._ime_editing_text) == 0:
                        self._ime_editing = False
                    continue

                if event.key == pg.K_BACKSPACE:
                    if len(self._ime_text) > 0 and self._ime_text_pos > 0:
                        self._ime_text = (
                            self._ime_text[0 : self._ime_text_pos - 1]
                            + self._ime_text[self._ime_text_pos :]
                        )
                        self._ime_text_pos = max(0, self._ime_text_pos - 1)

                elif event.key == pg.K_DELETE:
                    self._ime_text = (
                        self._ime_text[0 : self._ime_text_pos]
                        + self._ime_text[self._ime_text_pos + 1 :]
                    )
                elif event.key == pg.K_LEFT:
                    self._ime_text_pos = max(0, self._ime_text_pos - 1)
                elif event.key == pg.K_RIGHT:
                    self._ime_text_pos = min(
                        len(self._ime_text), self._ime_text_pos + 1
                    )
                # Handle ENTER key
                elif event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                    # Block if we have no text to append
                    if len(self._ime_text) == 0:
                        continue

                    return self._ime_text

            elif event.type == pg.TEXTEDITING:
                if self.print_event:
                    print(event)
                self._ime_editing = True
                self._ime_editing_text = event.text
                self._ime_editing_pos = event.start

            elif event.type == pg.TEXTINPUT:
                if self.print_event:
                    print(event)
                self._ime_editing = False
                self._ime_editing_text = ""
                self._ime_text = (
                    self._ime_text[0 : self._ime_text_pos]
                    + event.text
                    + self._ime_text[self._ime_text_pos :]
                )
                self._ime_text_pos += len(event.text)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the text input widget onto the provided surface
        """

        # Chat box updates
        start_pos = self.CHAT_BOX_POS.copy()
        ime_text_l = self.prompt + self._ime_text[0 : self._ime_text_pos]
        ime_text_m = (
            self._ime_editing_text[0 : self._ime_editing_pos]
            + "|"
            + self._ime_editing_text[self._ime_editing_pos :]
        )
        ime_text_r = self._ime_text[self._ime_text_pos :]

        rect_text_l = self.font.render_to(
            screen, start_pos, ime_text_l, self.text_color
        )
        start_pos.x += rect_text_l.width

        # Editing texts should be underlined
        rect_text_m = self.font.render_to(
            screen,
            start_pos,
            ime_text_m,
            self.text_color,
            None,
            freetype.STYLE_UNDERLINE,
        )
        start_pos.x += rect_text_m.width
        self.font.render_to(screen, start_pos, ime_text_r, self.text_color)


    def draw_text(self, screen, pos, text):
        """
        Draws the text input widget onto the provided surface
        """
        self.font.render_to(screen, pos, text, self.text_color)

class TextInputGame:
    """
    A class that handles the game's events, mainloop etc.
    """

    # CONSTANTS
    # Frames per second, the general speed of the program
    FPS = 50

    def __init__(self, caption: str) -> None:
        # Initialize
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()

        # Text input
        # Set to true or add 'showevent' in argv to see IME and KEYDOWN events
        self.print_event = "showevent" in sys.argv
        self.text_input = TextInput(
            prompt="Enter a username: ",
            pos=(0, 20),
            screen_dimensions=(WINDOW_WIDTH, WINDOW_HEIGHT),
            print_event=self.print_event,
            text_color=BLUE,
        )

    def main_loop(self):
        pg.key.start_text_input()
        input_rect = pg.Rect(80, 80, 320, 40)
        pg.key.set_text_input_rect(input_rect)

        while True:
            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                elif event.type == pygame.locals.KEYDOWN:
                    if event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                        username = self.text_input.update(events)
                        self.screen.fill(BLACK)
                        self.text_input.draw_text(self.screen, (0,20), "Welcome {}!".format(username))
                        self.text_input.draw_text(self.screen, (0,WINDOW_HEIGHT/2), "Waiting for another player to join")
                        pg.display.update()
                        return username

            self.text_input.update(events)

            # # Screen updates
            self.screen.fill(BLACK)
            self.text_input.draw(self.screen)

            pg.display.update()