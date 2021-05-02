""" May 2, 2021 """

import pygame
import math as m
from setup.settings import Settings
from setup.printr import Printr


class Node:

    def __init__(self, win, id, x, y):
        pygame.init()
        self.win = win
        self.set = Settings()
        self.printr = Printr(self.win)

        self.ID = id ## Unique string, from A-ZZ
        self.x, self.y = x, y
        self.r = 20
        self.suppress_hovering = True

        ## Colours
        self.c = self.set.grey
        self.hover_c = self.set.dark_grey
        self.make_edge_c = self.set.red

        ## Flags
        self.hovering = False
        self.moving = False
        self.making_edge_start = False


    def get_ID(self):
        return self.ID

    def get_coords(self):
        return (self.x, self.y)


    """ DRAWING """
    def draw(self):
        self.draw_circle()
        self.draw_ID()

    def draw_circle(self):
        c = self.c
        if self.hovering:
            c = self.hover_c

        pygame.draw.circle(self.win, c, (self.x, self.y), self.r, 0)

        if self.making_edge_start:
            c = self.set.light_grey
            pygame.draw.circle(self.win, c, (self.x, self.y), self.r+3, 3)

    def draw_ID(self):
        c = self.set.white

        x, y = self.x, self.y
        x -= 4
        y -= 9

        ### Shift double-digit letters further over
        if len(self.ID) > 1:
            x -= 3

        text = self.set.large_font.render(self.ID, True, c)
        self.win.blit(text, (x, y))


    """ Making edge """
    def edge_start(self):
        self.making_edge_start = False

        if self.hovering:
            self.making_edge_start = True
            return True

        return False

    def edge_end(self):
        if self.hovering:
            if not self.making_edge_start:
                return True

        return False

    def cancel_edge_start(self):
        self.making_edge_start = False


    """ Moving """
    def start_moving(self):
        if self.hovering:
            self.moving = True

    def stop_moving(self):
        self.moving = False

    def move(self):
        if self.moving:
            mx, my = pygame.mouse.get_rel()
            self.x += mx
            self.y += my

    """ Hovering """
    def update_hovering(self, mx, my):
        self.hovering = False
        x, y = self.x, self.y
        euclid = m.sqrt( (mx-x)**2 + (my-y)**2 )

        if self.r > euclid:
            if not self.suppress_hovering:
                self.hovering = True
        else:
            self.suppress_hovering = False ## Don't 'hover' when node is created

    def get_hovering(self):
        return self.hovering



    """ Tracer """
    ## TRACER
    # text = str(round(euclid, 0)) + " | " + str(self.r) + " | " + str(self.hovering)
    # self.printr.tracer_printr(text, x+30, y, self.set.light_blue)
