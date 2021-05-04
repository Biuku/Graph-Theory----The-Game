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

        ## Algo stuff
        self.total_cost = m.inf
        self.unvisited = True
        self.parent = None

        ## Node objects this node is connected to where this is the start node
        self.neighbours = []

        ## Colours
        self.c = self.set.grey

        ## Flags
        self.hovering = False
        self.moving = False
        self.edge_start_node = False

        self.algo_start_node = False
        self.algo_end_node = False
        self.visiting = False
        self.looking_as_neighbour = False
        self.unvisited = True


    def get_coords(self):
        return (self.x, self.y)

    def get_ID(self):
        return self.ID


    """ Algo stuff """

    def set_total_cost(self, tc):
        self.total_cost = tc

    def get_total_cost(self):
        return self.total_cost


    def set_parent(self, node):
        self.parent = node

    def get_parent(self):
        return self.parent


    def set_visiting(self):
        self.visiting = True

    def cancel_visiting(self):
        self.visiting = False


    def set_looking_as_neighbour(self):
        self.looking_as_neighbour = True

    def cancel_looking_as_neighbour(self):
        self.looking_as_neighbour = False



    def set_unvisited(self):
        self.unvisited = False

    def get_unvisited(self):
        return self.unvisited



    """ SETTING START AND END NODES FOR ALGORITHM """
    def set_algo_start(self):
        self.algo_start_node = True
        self.total_cost = 0

    def get_algo_start(self):
        return self.algo_start_node

    def cancel_algo_start(self):
        self.algo_start_node = False


    def set_algo_end(self):
        self.algo_end_node = True

    def get_algo_end(self):
        return self.algo_end_node

    def cancel_algo_end(self):
        self.algo_end_node = False



    """
    Edges: all 'neighbours' are end nodes, where this is the start node
    """

    def set_edge_start_node(self):
        self.edge_start_node = True

    def cancel_edge_start(self):
        self.edge_start_node = False


    def add_neighbour(self, node):
        self.neighbours.append(node)

    def remove_neighbour(self, node):
        self.neighbours.remove(node)

    def get_neighbours(self):
        return self.neighbours


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




    """ DRAWING """
    def draw(self):
        self.draw_circle()
        self.draw_ID()
        self.draw_weight()

    def draw_circle(self):
        c = self.get_colour()

        pygame.draw.circle(self.win, c, (self.x, self.y), self.r, 0)

        if self.edge_start_node or self.hovering:
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


    def draw_weight(self):
        c = self.set.white
        x, y = self.x, self.y
        x += (self.r + 5)
        y -= 20

        pygame.draw.rect(self.win, self.set.background, pygame.Rect(x, y, 40, 20), 0)

        x += 5
        y += 3

        text = "w: " + str(round(self.total_cost, 1))
        text = self.set.small_font.render(text, True, c)
        self.win.blit(text, (x, y))


    def get_colour(self):
        if not self.unvisited:
            return self.set.blue
        if self.visiting:
            return self.set.yellow
        if self.looking_as_neighbour:
            return self.set.dark_orange

        if self.algo_start_node:
            return self.set.green
        if self.algo_end_node:
            return self.set.black


        return self.c
