""" May 2, 2021 """

import pygame
from setup.settings import Settings
from setup.pygameBasics import PygameBasics
from setup.printr import Printr
from node import Node


class Main(PygameBasics):
    def __init__(self):
        pygame.init()
        super().__init__()

        self.win_w, self.win_h  = 1600, 900
        self.win = pygame.display.set_mode((self.win_w, self.win_h), pygame.RESIZABLE)

        self.printr = Printr(self.win)
        self.nodes = {}

        ## Flags
        self.edge_start_node = False

    """ EVENTS """

    def left_click_events(self):
        pygame.mouse.get_rel() ## Reset pygame relative mouse position
        self.start_moving()

    def right_click_events(self):
        pass

    def mouse_button_up_events(self):
        self.stop_moving()


    def keydown_events(self, event):
        if event.key == pygame.K_SPACE:
            self.make_node()

        if event.key == pygame.K_e:
            self.make_edge()

        if event.key == pygame.K_p:
            pass
            # Tracer

        if event.key == pygame.K_q:
            pygame.quit(), quit()


    def keyup_events(self, event):
        pass

    """ Conditional events """

    def make_node(self):
        id = self.set.get_node_id()
        mx, my = pygame.mouse.get_pos()

        node = Node(self.win, id, mx, my)
        self.nodes[node] = []

    def start_moving(self):
        for node in self.nodes.keys():
            node.start_moving()

    def stop_moving(self):
        for node in self.nodes.keys():
            node.stop_moving()


    def make_edge(self):
        """ Called by pressing 'e' """

        ## If we haven't yet picked the start of our edge
        if not self.edge_start_node:
            for node in self.nodes.keys():
                if node.edge_start():
                    self.edge_start_node = node
                    break

        ## If we previously picked a start node, look for an end node
        else:
            for node in self.nodes.keys():
                if node.edge_end():
                    self.nodes[self.edge_start_node].append( [node, 1] )
                    self.edge_start_node.cancel_edge_start()
                    self.edge_start_node = False
                    break


    """ UPDATES """

    def updates(self):
        self.update_hovering()
        self.move()
        self.draw()


    def update_hovering(self):
        mx, my = pygame.mouse.get_pos()

        for node in self.nodes.keys():
            node.update_hovering(mx, my)

    def move(self):
        for node in self.nodes.keys():
            node.move()


    def draw(self):

        self.draw_page_border()
        self.draw_working_area_border()
        self.printr.print_instructions(self.edge_start_node)
        self.draw_edges()
        self.draw_nodes()

        pygame.display.update()

    def draw_edges(self):
        c = self.set.grey
        for node, edges in self.nodes.items():
            start_coord = node.get_coords()

            for end_node in edges:
                end_coord = end_node[0].get_coords()
                pygame.draw.line(self.win, c, start_coord, end_coord, 1)

    def draw_nodes(self):
        for node in self.nodes.keys():
            node.draw()




    """ MAIN """

    def main(self):
        while True:
            self.set.clock.tick(self.set.FPS)
            self.win.fill(self.set.background)
            self.events()
            self.updates()

if __name__ == "__main__":
    x = Main()
    x.main()
