import pygame
import random
import time

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (255, 0, 255)
GRAMA = (146, 199, 93)
CORTADOR = (96, 170, 196)
CHECKPOINT_COLOR = (224, 161, 79)

FPS = 60
WIDTH = 800

class Gui():
    def __init__(self, coords):
        # gui variables
        self.grid_size = 15
        self.box_width = WIDTH/self.grid_size
        self.coords = coords
        self.placing_walls = False
        self.removing_walls = False
        self.animation_speed = 5

        self.coords.maze = [
            [0 for x in range(self.grid_size)] for y in range(self.grid_size)]

        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, WIDTH))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("GramaZen - Visualização")

    # main function for gui
    def main(self, running=False):
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

        if not running:
            if self.placing_walls == True:
                self.place_wall()
            elif self.removing_walls == True:
                self.remove()

        self.event_handle(running)
        self.redraw()
        pygame.display.update()
        

    def event_handle(self, running):
        run_keys = {"q"}
        checkpoint_keys = {"1", "2"}

        for event in pygame.event.get():
            try:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # key presses
                elif event.type == pygame.KEYDOWN:
                    #
                    # Verificações no teclado.
                    # Verifica se não tem nenhum algoritmo rodando. Se não tiver, pode usar as teclas do teclado.
                    #
                    key = chr(event.key)

                    if running == False:
                        # run algorithm 
                        if key in run_keys:
                            self.run_algorithm(key)              
                        
                        elif key == "x":
                            self.coords.remove_all()
                            
                        elif key == "z":
                            self.coords.remove_last()
                            
                        elif key in checkpoint_keys:
                            self.place_check_point(key)

                        elif key == " ":
                            self.coords.generate_random_maze(gui)


                    elif (key == "+" or key == "=") and self.animation_speed > 0:
                        if self.animation_speed <= 2:
                            self.animation_speed = 1
                        else:
                            self.animation_speed = int(self.animation_speed * 0.5) + 1

                    elif key == "-":
                        self.animation_speed = int(self.animation_speed * 2) + 1

                    else:
                        print(key)


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #
                    # Quando aperta os botões do mouse, inicia a lógica para colocar, ou remover, paredes.
                    #
                    if running == False:
                        if event.button == 1:
                            self.placing_walls = True

                        elif event.button == 3:
                            self.removing_walls = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    #
                    # Quando "desaperta" os botões do mouse, inicia a lógica para colocar, ou remover, paredes.
                    #

                    if event.button == 1:
                        self.placing_walls = False

                    elif event.button == 3:
                        self.removing_walls = False
            
            except ValueError:
                print("Closing game due to key mismatch.")
                pygame.quit()
                exit()
            
            except Exception:
                print("Closing game due to unknown error.")
                pygame.quit()
                exit()


    def redraw(self):
        self.win.fill(GRAMA)
        self.draw_points()
        self.draw_grid()


    def draw_grid(self):
        for i in range(self.grid_size-1):
            pygame.draw.rect(
                self.win,
                BLACK,
                ((i+1)*self.box_width-2, 0, 5, WIDTH)
            )
            pygame.draw.rect(
                self.win,
                BLACK,
                (0, (i+1)*self.box_width-2, WIDTH, 5)
            )


    def draw_points(self):
        # Desenhando os vizinhos
        for node in self.coords.open_list:
            self.draw_box(node.position, GREEN)

        # Desenhando os que já foram visitados
        for node in self.coords.closed_list:
            self.draw_box(node.position, BLUE)

        # Desenha o caminho final (meio desnecessário pra mim)
        for wall in self.coords.final_path:
            self.draw_box(wall, PINK)

        # Pintando as paredes
        for wall in self.coords.walls:
            self.draw_box(wall, BLACK)

        # Pintando os checkpoints
        for num, point in enumerate(self.coords.check_points):
            if point != None:
                self.draw_box(point, CHECKPOINT_COLOR)
                self.display_text(
                    str(num+1),
                    WHITE,
                    self.box_center(point),
                    int(self.box_width)
                )
        
        if self.coords.start != None:
            self.draw_box(self.coords.start, (255, 0, 0))
            self.display_text(
                "S",
                WHITE,
                self.box_center(self.coords.start),
                int(self.box_width)
            )

            
        if self.coords.end != None:
            self.draw_box(self.coords.end, (255, 0, 0))
            self.display_text(
                "E",
                WHITE,
                self.box_center(self.coords.end),
                int(self.box_width)
            )


    def box_center(self, box):
        box_x, box_y = box
        center = ((box_x*self.box_width + self.box_width/2),
                  (box_y*self.box_width + self.box_width/2))

        return center


    def draw_box(self, box, colour):
        box_x, box_y = box
        pygame.draw.rect(
            self.win,
            colour,
            (
                box_x * self.box_width,
                box_y * self.box_width,
                self.box_width,
                self.box_width
            )
        )


    def get_box_coords(self):
        box_x = int((self.mouse_x + 2) / self.box_width)
        box_y = int((self.mouse_y + 2) / self.box_width)
        return (box_x, box_y)



    def place_check_point(self, index):
        coords = self.get_box_coords()
        if (coords != self.coords.start
            and coords != self.coords.end
            and coords not in self.coords.walls
            and coords not in self.coords.check_points):

            while len(self.coords.check_points) <= int(index)-1:
                self.coords.check_points.append("None")

            self.coords.check_points[int(index)-1] = coords


    def place_wall(self):
        coords = self.get_box_coords()
        if (coords != self.coords.start
            and coords != self.coords.end
            and coords not in self.coords.walls
            and coords not in self.coords.check_points):
            self.coords.walls.append(coords)


    def remove(self):
        coords = self.get_box_coords()
        if coords in self.coords.walls:
            self.coords.walls.remove(coords)

        elif coords in self.coords.check_points:
            self.coords.check_points.remove(coords)

        elif coords == self.coords.start:
            self.coords.start = None

        elif coords == self.coords.end:
            self.coords.end = None


    def run_algorithm(self, key):
        self.placing_walls = False
        self.removing_walls = False
        self.coords.remove_last()

        if len(self.coords.check_points) > 1:
            self.coords.create_maze(gui)
            check_points = self.coords.check_points[:]
            check_points = [point for point in check_points if point != "None"]

            for i, point in enumerate(check_points):
                if i != len(check_points)-1:
                    start = point
                    end = check_points[i+1]

                    new_path = pathfind(
                        self.coords.maze,
                        start,
                        end,
                        self,
                        self.coords,
                        key
                    )

                    if new_path == None:
                        new_path = []

                    self.coords.final_path.extend(new_path)


    def display_text(self, txt, colour, center, size):
        font = pygame.font.Font(None, size)
        text_surf = font.render(txt, True, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (center)
        self.win.blit(text_surf, text_rect)


class Coordinates():
    def __init__(self):
        self.remove_all()


    def remove_all(self):
        self.start = None
        self.end = None
        self.walls = []
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []
        self.check_points = []


    def remove_last(self):
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []


    def largest_distance(self):
        largest = 0

        for wall in self.walls:
            if wall[0] > largest:
                largest = wall[0]

            if wall[1] > largest:
                largest = wall[1]

        for point in self.check_points:
            if point[0] > largest:
                largest = point[0]

            if point[1] > largest:
                largest = point[1]

        return largest + 1


    def create_maze(self, gui):
        largest = self.largest_distance()

        if gui.grid_size > largest:
            largest = gui.grid_size

        self.maze = [[0 for x in range(largest)] for y in range(largest)]
        for wall in self.walls:
            try:
                wall_x, wall_y = wall
                self.maze[wall_x][wall_y] = 1
            except:
                pass


    def generate_random_maze(self, gui):
        self.walls = []
        for _ in range(gui.grid_size*gui.grid_size):
            if random.random() > 0.6:
                wall = (random.randint(0, gui.grid_size-1),
                        random.randint(0, gui.grid_size-1))
                if wall not in self.walls:
                    self.walls.append(wall)


def pathfind(maze, start, end, gui, coords, key):
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    closed_list = []

    open_list.append(start_node)

    count = 0 

    # Loop until you find the end
    while len(open_list) > 0:
        if count >= gui.animation_speed:
            count = 0

            if key == "q":
                current_node = open_list[-1]
                current_index = len(open_list)-1

            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                coords.open_list = open_list
                coords.closed_list = closed_list
                return path

            for new_pos in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                node_pos = (current_node.position[0] + new_pos[0],
                            current_node.position[1] + new_pos[1])

                if (
                    node_pos[0] > (len(maze) - 1)
                    or node_pos[0] < 0
                    or node_pos[1] > (len(maze[len(maze)-1]) -1)
                    or node_pos[1] < 0
                ):
                    continue

                if maze[node_pos[0]][node_pos[1]] != 0:
                    continue

                if Node(current_node, node_pos) in closed_list:
                    continue

                child = Node(current_node, node_pos)
                
                passList = [
                    False
                    for closed_child in closed_list
                    if child == closed_child
                ]
                if False in passList:
                    continue
          
                for open_node in open_list:
                    pass

                else:
                    open_list.append(child)

        else:
            coords.open_list = open_list
            coords.closed_list = closed_list
            gui.main(True)

        count += 1


class Node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

if __name__ == "__main__":
    time.sleep(0.1)
    gui = Gui(Coordinates())
    while True:
        gui.main()