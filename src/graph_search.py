from get_neighbors import get_neighbors, is_neighbor
from node import Node
from coordinates import Coordinates


def dfs(maze, start, end, gui, coords: Coordinates, key):
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

            if not is_neighbor(current_node, open_list[-1]):
                current_node = current_node.parent
                continue

            current_node = open_list.pop()
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
