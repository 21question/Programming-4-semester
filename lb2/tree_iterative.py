
def bin_tree_iterative(root=2, height=6, left_leaf=lambda r: r*3, right_leaf=lambda r: r+4):
    if height <= 0:
        return None

    from collections import deque
    tree = {"value": root, "left": None, "right": None}
    queue = deque()
    queue.append((tree, root, 1))

    while queue:
        node, current_value, current_depth = queue.popleft()

        if current_depth >= height:
            continue

        left_val = left_leaf(current_value)
        right_val = right_leaf(current_value)

        left_node = {"value": left_val, "left": None, "right": None}
        right_node = {"value": right_val, "left": None, "right": None}

        node["left"] = left_node
        node["right"] = right_node

        queue.append((left_node, left_val, current_depth + 1))
        queue.append((right_node, right_val, current_depth + 1))

    return tree
