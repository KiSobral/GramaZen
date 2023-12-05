from get_neighbors import get_neighbors
from node import Node
from coordinates import Coordinates


def pathfind(maze, start, end, gui, coords: Coordinates, key):
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    closed_list = []

    open_list.append(start_node)
    current_node = start_node

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

            node_positions = [
                (current_node.position[0] + new_pos[0],
                 current_node.position[1] + new_pos[1])
                for new_pos in [(-1, 0), (0, 1), (1, 0), (0, -1)]
            ]

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                coords.open_list = open_list
                coords.closed_list = closed_list
                return path

            for neighbor in get_neighbors(current_node):
                if (
                    neighbor.position[0] > (len(maze) - 1)
                    or neighbor.position[0] < 0
                    or neighbor.position[1] > (len(maze[len(maze)-1]) -1)
                    or neighbor.position[1] < 0
                ):
                    continue

                if maze[neighbor.position[0]][neighbor.position[1]] != 0:
                    continue

                if neighbor in closed_list:
                    continue
                
                pass_list = [
                    False
                    for closed_child in closed_list
                    if neighbor == closed_child
                ]
                if False in pass_list:
                    continue
          
                for i, open_check in enumerate(open_list):
                    if neighbor == open_check:
                        open_list.pop(i)
                        break

                open_list.append(neighbor)

        else:
            coords.current_node = current_node
            coords.open_list = open_list
            coords.closed_list = closed_list
            gui.main(True)

        count += 1
