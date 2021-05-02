""" April 29, 2021 """

import pygame


class Settings:

    def __init__(self):


        self.border_gap = 0.02 ## Gap in % from screen edge to drawn screen border
        self.working_area_border = 0.67 ## Line demarcating plot area from working area

        self.clock = pygame.time.Clock()
        self.FPS = 250

        ### Colours
        self.white, self.black = (255, 255, 255), (0, 0, 0)
        self.ultra_light_grey = (240, 240, 240)
        self.light_grey, self.grey, self.dark_grey = (221, 221, 221), (150,150,150), (45, 45, 45)

        self.blue, self.light_blue = (190, 170, 255), (210, 210, 255)
        self.red, self.light_red = (255, 0, 0), (255, 175, 175)

        self.background = (20, 20, 20) #self.black

        ### Fonts
        self.small_font = pygame.font.SysFont('lucidasans', 10)
        self.med_font = pygame.font.SysFont('lucidasans', 11)
        self.large_font = pygame.font.SysFont('lucidasans', 12)

        self.node_IDs = self.make_node_ids_stack()


    """ NODE NAMES """

    def get_node_id(self):
        return self.node_IDs.pop(0)

    def make_node_ids_stack(self):
        alpha = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        stack = alpha[:]

        for i in range(0, len(alpha)):
            for j in range(len(alpha)):
                stack.append(alpha[i] + alpha[j])

        return stack


    def reset_node_ids_stack(self):
        self.node_names = self.make_node_ids_stack()
