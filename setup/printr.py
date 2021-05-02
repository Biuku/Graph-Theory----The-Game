""" April 29, 2021 """

import pygame
import math as m
import random as r
from setup.settings import Settings


class Printr:
    def __init__(self, win):
        pygame.init()
        self.win = win
        self.set = Settings()

        self.update_screen()

    def tracer_printr(self, data, x, y, c):
        text = self.set.med_font.render(data, True, c)
        self.win.blit( text, (x, y) )

    def update_screen(self):
        """ ??? Do I need to update self.win here as well??? """
        self.win_w = self.win.get_width()
        self.win_h = self.win.get_height()

        side_cushion = 2 ## in percent
        top_cushion = 3 ## in percent

        self.left_cushion = self.win_w * (self.set.working_area_border + side_cushion/100)
        self.top_cushion = self.win_h * (self.set.border_gap + top_cushion/100)


    def print_instructions(self, start_edge):
        ## Set area

        x = self.left_cushion
        y = self.top_cushion

        texts = [
            'INSTRUCTIONS',
            '  · Click = move',
            '  · New node: double-click',
            '  · New edge: double-click a node',
            '  · Show adjacency matrix: M',
            '  · Re-alphabeticalize nodes: A',
            '  · Quit: Q',
            '',
            'SOME GRAPH DATA',
            '  · Start edge: ' + str(start_edge),
            '  · TBD:  ',
            '  · TBD:  ',
            ]


        for text in texts:
            print_instructions = self.set.med_font.render(text, True, self.set.light_grey)
            self.win.blit( print_instructions, (x, y) )
            y += 22
