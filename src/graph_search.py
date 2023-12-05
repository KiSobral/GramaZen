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

            for node_pos in node_positions:
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
                
                pass_list = [
                    False
                    for closed_child in closed_list
                    if child == closed_child
                ]
                if False in pass_list:
                    continue
          
                for i, open_check in enumerate(open_list):
                    if child == open_check:
                        open_list.pop(i)
                        break

                open_list.append(child)

        else:
            coords.current_node = current_node
            coords.open_list = open_list
            coords.closed_list = closed_list
            gui.main(True)

        count += 1
