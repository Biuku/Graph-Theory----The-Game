""" MAY 1, 2021 """

import pygame
from setup.settings import Settings

class PygameBasics:
    def __init__(self):
        pygame.init()
        self.set = Settings()


    """ EVENTS """

    def events(self):
        for event in pygame.event.get():


            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.left_click_events()

                if pygame.mouse.get_pressed()[2]:
                    self.right_click_events()

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_up_events()

            elif event.type == pygame.KEYDOWN:
                self.keydown_events(event)

            elif event.type == pygame.KEYUP:
                self.keyup_events(event)

            elif event.type == pygame.VIDEORESIZE:
                self.update_window_size(event)

            elif event.type == pygame.QUIT:
                pygame.quit(), quit()



    """ Draw background """

    def draw_page_border(self):
        """ Draw rectangle around the entire page to give it an edge """

        x = self.win_w * self.set.border_gap
        y = self.win_h * self.set.border_gap

        w =  self.win_w * (1 - (2 * self.set.border_gap))
        h = self.win_h * (1 - (2 * self.set.border_gap))

        c = self.set.grey
        thick = 2

        pygame.draw.rect(self.win, c, pygame.Rect(x, y, w, h), thick)


    def draw_working_area_border(self):
        """ Draw line demarcating plotting area from instructions and meta graph info """
        c = self.set.blue
        x = self.win_w * self.set.working_area_border
        top = self.win_h * self.set.border_gap + 1
        bot = self.win_h * (1 - self.set.border_gap) - 1

        pygame.draw.line(self.win, c, (x, top), (x, bot), 2)
