""" April 29, 2021 """

import pygame
import math as m
from setup.printr import Printr
from arr import Arr
from plot import Plot
from drawline import DrawLine


class Algo(Arr):
    def __init__(self, win):
        pygame.init()
        self.win = win
        super().__init__()

        self.printr = Printr(self.win)
        self.plot = Plot(self.win)
        self.drawline = DrawLine(self.win)

        ### Try to do everything in array units, then convert only to move and draw
        self.mid = [50, 12] ## Could base off the centre of the scale
        self.slope = 1
        self.degrees = 45
        self.hypoteneuse = 300
        self.update_coordinates() ## do this once to get start/end


    def update(self, motion, display):
        self.moving, self.rotating = motion
        self.show_centroid, self.show_intercepts = display
        self.move()
        self.rotate()


    def move(self):
        if self.moving:
            px, py = self.convert_arr_to_pixels(self.mid)
            mx, my = pygame.mouse.get_rel()

            px += mx
            py += my

            self.mid = self.convert_pixel_to_arr( (px, py) )
            self.update_coordinates()


    def rotate(self):
        if self.rotating:
            self.degrees += self.rotating

            if self.degrees > 360:
                self.degrees = 1
            if self.degrees < 0:
                self.degrees =  359

            self.slope = m.tan(m.radians(self.degrees))
            self.update_coordinates()


    def update_coordinates(self):
        self.update_end_points()

        self.px_mid = tuple( self.convert_arr_to_pixels(self.mid) )
        self.px_start = tuple( self.convert_arr_to_pixels(self.start) )
        self.px_end = tuple (self.convert_arr_to_pixels(self.end) )


    def update_end_points(self):
        """ Update the start and end points if line moves/rotates"""
        """ Must do in pixel units because the scale doesn't allow line length to be converted, just points"""

        midx, midy = self.convert_arr_to_pixels(self.mid)
        #theta = m.atan(self.slope) ## in radians
        theta = m.radians(self.degrees) ## in radians

        ## Do trig
        opp = m.sin(theta) * self.hypoteneuse
        adj = m.cos(theta) * self.hypoteneuse

        ## Get start/end by applying deltas to mid coord
        start_x = int(midx - adj)
        start_y = int(midy + opp)
        end_x = int(midx + adj)
        end_y = int(midy - opp) # account for pygame negative stupidity

        self.start = self.convert_pixel_to_arr( (start_x, start_y) )
        self.end = self.convert_pixel_to_arr( (end_x, end_y) )


    """ Regression stuff """

    def update_coefficients(self):
        ## Slope
        # x1, y1 = self.arr_mid
        # x2, y2 = self.arr_start
        # if x2-x1 != 0:
        #     self.slope = (y2 - y1) / (x2-x1)

        ## Y intercept
        self.y_intercept = y2 - self.slope*x2
        b0_mid = y1 - self.slope*x1




    def draw(self):
        self.plot.draw(self.points)
        # self.draw_line()
        self.drawline.draw(self.mid, self.px_mid, self.px_start, self.px_end)

        self.printr.print_instructions(1, 1, 1, 1, self.slope, self.degrees, 1)  # b0, b1, SSE, y_int, slope, degrees, sse



    def configure_plot(self):
        self.plot.configure_scales(self.arr_scale, self.pixel_scale, self.pixel_w, self.pixel_h)
