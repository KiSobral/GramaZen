from typing import Tuple
import pygame

from coordinates import Coordinates
from graph_search import dfs
from consts import *


class Gui():
    grid_size: int
    box_width: float
    coords: Coordinates
    placing_blocks: bool
    removing_blocks: bool
    cut_speed: int


    def __init__(self, coords):
        self.grid_size = 15
        self.box_width = WIDTH/self.grid_size
        self.coords = coords
        self.placing_blocks = False
        self.removing_blocks = False
        self.cut_speed = 15

        self.coords.maze = [
            [0 for _ in range(self.grid_size)]
            for __ in range(self.grid_size)]

        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, WIDTH))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_TITLE)


    def sprite(self, is_running=False):
        '''
        Essa função fica rodando em loop. Enquanto o loop estiver ativo, o jogo está rodando.
        Os passos que essa função faz:
            1. tick do clock do jogo
            2. Pega posição do mouse
            3. Verifica alocação de obstáculos (remove ou coloca paredes)
            4. Trata dos eventos assíncronos (clique do mouse, digitar do teclado)
            5. Redesenha a grid do jogo
        '''
        self.clock.tick(FPS)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        if not is_running:
            if self.placing_blocks == True:
                self.place_wall()
            elif self.removing_blocks == True:
                self.remove()

        self.event_handle(is_running)
        self.redraw()
        pygame.display.update()
        

    def event_handle(self, running):
        run_keys = set("q")
        checkpoint_keys = set("1")
        clear_field_keys = set("x")
        clear_cut_keys = set("z")
        random_blocks_keys = set(" ")
        speed_up_keys = set(["+", "="])
        slow_down_keys = set("-")
        stop_cutter_keys = set("p")

        for event in pygame.event.get():
            try:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    key = chr(event.key)

                    if not running:
                        if key in run_keys:
                            self.run_algorithm()              

                        elif key in clear_field_keys:
                            self.coords.clear_all_field()

                        elif key in clear_cut_keys:
                            self.coords.clear_cut()

                        elif key in checkpoint_keys:
                            self.place_start()

                        elif key in random_blocks_keys:
                            self.coords.generate_random_blocks(self)

                    if key in speed_up_keys and self.cut_speed > 0:
                        if self.cut_speed <= 2:
                            self.cut_speed = 2
                        else:
                            self.cut_speed = int(self.cut_speed * 0.5) + 1

                    elif key in slow_down_keys:
                        self.cut_speed = int(self.cut_speed * 2) + 1

                    elif key in stop_cutter_keys:
                        # Altera o estado de is_running no singleton
                        pass

                    else:
                        print(key)


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if running == False:
                        if event.button == 1: # Alias de estado da pygame
                            self.placing_blocks = True

                        elif event.button == 3: # Alias de estado da pygame
                            self.removing_blocks = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: # Alias de estado da pygame
                        self.placing_blocks = False

                    elif event.button == 3: # Alias de estado da pygame
                        self.removing_blocks = False
            
            except ValueError:
                print("Key mismatch.")
                pygame.quit()
                exit()
            
            except Exception:
                print("Closing game due to unknown error.")
                pygame.quit()
                exit()


    def redraw(self):
        self.window.fill(GRASS)
        self.draw_points()
        self.draw_grid()


    def draw_grid(self):
        for i in range(self.grid_size-1):
            pygame.draw.rect(
                self.window,
                BLACK,
                ((i+1)*self.box_width-2, 0, 5, WIDTH)
            )
            pygame.draw.rect(
                self.window,
                BLACK,
                (0, (i+1)*self.box_width-2, WIDTH, 5)
            )


    def draw_points(self):
        for node in self.coords.open_list:
            self.draw_box(node.position, TO_VISIT)

        for node in self.coords.closed_list:
            self.draw_box(node.position, CUT_GRASS)

        if self.coords.current_node is not None:
            self.draw_box(self.coords.current_node.position, CUTTER)

        for wall in self.coords.walls:
            self.draw_box(wall, BLACK)

        if self.coords.start_point:
            self.draw_box(
                self.coords.start_point,
                START_COORD
            )


    def box_center(self, box):
        box_x, box_y = box
        center = ((box_x*self.box_width + self.box_width/2),
                  (box_y*self.box_width + self.box_width/2))
        return center


    def draw_box(self, box, colour):
        box_x, box_y = box
        pygame.draw.rect(
            self.window,
            colour,
            (
                box_x * self.box_width,
                box_y * self.box_width,
                self.box_width,
                self.box_width
            )
        )


    def get_box_coords(self) -> Tuple[int, int]:
        box_x = int((self.mouse_x + 2) / self.box_width)
        box_y = int((self.mouse_y + 2) / self.box_width)
        return (box_x, box_y)


    def place_start(self):
        box_coords = self.get_box_coords()
        if box_coords not in self.coords.walls:
            self.coords.start_point = box_coords


    def place_wall(self):
        coords = self.get_box_coords()
        if (coords != self.coords.start
            and coords not in self.coords.walls):
            self.coords.walls.append(coords)


    def remove(self):
        coords = self.get_box_coords()
        if coords in self.coords.walls:
            self.coords.walls.remove(coords)

        elif coords == self.coords.start_point:
            self.coords.start_point = None

        elif coords == self.coords.start:
            self.coords.start = None


    def run_algorithm(self):
        self.placing_blocks = False
        self.removing_blocks = False
        self.coords.clear_cut()

        if self.coords.start_point:
            self.coords.create_maze(self)
            dfs(
                self.coords.maze,
                self.coords.start_point,
                self,
                self.coords,
            )
