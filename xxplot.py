""" April 28, 2021 """

import pygame
from setup.settings import Settings
from setup.printr import Printr


class Plot:

    def __init__(self, win):
        pygame.init()
        self.win = win
        self.printr = Printr(self.win)
        self.set = Settings()

        self.c1 = self.set.ultra_light_grey
        self.c2 = self.set.grey
        self.c3 = self.set.dark_grey


    def draw(self, points):
        self.draw_axes()
        self.draw_x_axis_labels()
        self.draw_y_axis_labels()
        self.draw_observations(points)

    def draw_observations(self, points):
        for point in points:
            point.draw()


    def draw_axes(self):
        x, y = self.pixel_origin
        right = x + self.pixel_w
        top = y - self.pixel_h

        pygame.draw.line(self.win, self.c3, (x, y), (x, top), 2)
        pygame.draw.line(self.win, self.c3, (x, y), (right, y), 2)


    def draw_x_axis_labels(self):
        y = self.pixel_origin[1]

        for i in range(len(self.pixel_scale)):
            x = self.pixel_scale[i,0]
            arr = self.arr_scale[i,0]
            self.draw_axis_labels(x-5, y+10, arr, x)
            pygame.draw.circle(self.win, self.c1, (x, y+1), 2, 0)


    def draw_y_axis_labels(self):
        x = self.pixel_origin[0]

        for i in range(len(self.pixel_scale)):
            y = self.pixel_scale[i,1]
            arr = self.arr_scale[i,1]
            self.draw_axis_labels(x-35, y-8, arr, y)
            pygame.draw.circle(self.win, self.set.grey, (x+1, y), 2, 0)


    def draw_axis_labels(self, x, y, arr_label, pixel_label):
        self.printr.axis_label_printr(round(arr_label, 1), x, y, self.c1)
        self.printr.axis_label_printr(int(pixel_label), x, y + 12, self.set.blue)


    """ UTILITY """
    def configure_scales(self, arr, px, w, h):
        self.arr_scale = arr
        self.pixel_scale = px
        self.pixel_origin = (px[0,0], px[0,1])
        self.pixel_w = w
        self.pixel_h = h
