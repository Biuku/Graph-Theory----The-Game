""" May 2, 2021 """

import pygame
import math
from setup.settings import Settings
from setup.pygameBasics import PygameBasics
from setup.printr import Printr
from node import Node


class Main(PygameBasics):
    def __init__(self):
        pygame.init()
        super().__init__()

        self.win_w, self.win_h  = 1900, 950
        self.win = pygame.display.set_mode((self.win_w, self.win_h), pygame.RESIZABLE)
        self.printr = Printr(self.win)

        self.nodes = []
        self.queue = []

        self.algo_wait = False

        ## Object flags
        self.hover_node = False
        self.edge_start_node = False
        self.algo_start_node = False
        self.algo_end_node = False


    """ EVENTS """

    def left_click_events(self):
        pygame.mouse.get_rel() ## Reset pygame relative mouse position
        self.start_moving()
        self.make_node()

    def right_click_events(self):
        self.make_edge()


    def mouse_button_up_events(self):
        self.stop_moving()

    def keydown_events(self, event):
        if event.key == pygame.K_SPACE:
            self.make_node()

        if event.key == pygame.K_e:
            self.make_edge()

        if event.key == pygame.K_s:
            self.update_algo_start_node()

        if event.key == pygame.K_x:
            self.update_algo_end_node()

        if event.key == pygame.K_d:
            self.dijkstra()

        ## Tracer
        if event.key == pygame.K_p:
            for nb in self.algo_start_node.neighbours:
                print(nb.ID, nb.total_cost)

        if event.key == pygame.K_q:
            pygame.quit(), quit()

    def keyup_events(self, event):
        pass

    """ Conditional events """

    def make_node(self):
        if not self.hover_node:
            id = self.set.get_node_id()
            mx, my = pygame.mouse.get_pos()

            node = Node(self.win, id, mx, my)
            self.nodes.append(node)

    def start_moving(self):
        for node in self.nodes:
            node.start_moving()

    def stop_moving(self):
        for node in self.nodes:
            node.stop_moving()


    def make_edge(self):
        """ Called by pressing 'e' """

        ## If we haven't yet picked the start of our edge
        if not self.edge_start_node:
            if self.hover_node:
                self.hover_node.set_edge_start_node()
                self.edge_start_node = self.hover_node

        ## If we previously picked a start node, look for an end node
        else:
            if self.hover_node:
                self.edge_start_node.add_neighbour(self.hover_node)
                self.edge_start_node.cancel_edge_start()
                self.edge_start_node = False


    def update_algo_start_node(self):
        if self.hover_node:
            if self.algo_start_node:
                self.algo_start_node.cancel_algo_start()
                self.algo_start_node = False

            else:
                self.hover_node.set_algo_start()
                self.algo_start_node = self.hover_node

    def update_algo_end_node(self):
        if self.hover_node:
            if self.algo_end_node:
                self.algo_end_node.cancel_algo_end()
                self.algo_end_node = False

            else:
                self.hover_node.set_algo_end()
                self.algo_end_node = self.hover_node



    """ ******************** """

    def dijkstra(self):
        if not self.algo_start_node:
            return

        self.queue = [(0, self.algo_start_node)]
        print("Before loop: ", self.queue)

        while self.queue:
            self.curr_node = self.queue.pop(0)[1]
            self.curr_node.set_visiting()

            for self.nb in self.curr_node.get_neighbours():
                pygame.time.delay(1500)

                if self.nb.get_unvisited():
                    self.nb.set_looking_as_neighbour()

                    trial_weight = self.curr_node.get_total_cost() + self.get_euclid(self.curr_node, self.nb)

                    if trial_weight < self.nb.get_total_cost():
                        self.nb.set_total_cost(trial_weight)
                        self.nb.set_parent(self.curr_node)
                        self.queue.append( (trial_weight, self.nb))
                        self.queue.sort() ## Slow, but fine for less than a few thousand items

                self.draw()
                pygame.time.delay(1500)

                self.nb.cancel_looking_as_neighbour()

            self.draw()

            self.curr_node.set_unvisited()
            self.curr_node.cancel_visiting()


    def get_euclid(self, start, end):
        x1, y1 = start.get_coords()
        x2, y2 = end.get_coords()

        return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )



    """ UPDATES """

    def updates(self):
        self.update_hovering()
        self.move()
        self.draw()


    def update_hovering(self):
        self.hover_node = False
        mx, my = pygame.mouse.get_pos()

        for node in self.nodes:
            node.update_hovering(mx, my)
            if node.get_hovering():
                self.hover_node = node

    def move(self):
        for node in self.nodes:
            node.move()

    def draw(self):
        self.win.fill(self.set.background)
        self.draw_page_border()
        self.draw_working_area_border()
        self.printr.print_instructions(self.edge_start_node, self.hover_node, self.queue)
        self.draw_edges()
        self.draw_nodes()

        pygame.display.update()

    def draw_edges(self):
        c = self.set.grey
        for node in self.nodes:
            start_coord = node.get_coords()
            neighbours = node.get_neighbours()

            for end_node in neighbours:
                end_coord = end_node.get_coords()
                pygame.draw.line(self.win, c, start_coord, end_coord, 1)

    def draw_nodes(self):
        for node in self.nodes:
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
