from collections import deque

def bin_tree_iterative(root=2, height=6):


    if height <= 0:
        return None

    tree = {"value": root, "left": None, "right": None}
    queue = deque()
    queue.append((tree, root, 1))

    while queue:
        node, current_value, current_depth = queue.popleft()

        if current_depth >= height:
            continue

        left_val = current_value * 3
        right_val = current_value + 4

        left_node = {"value": left_val, "left": None, "right": None}
        right_node = {"value": right_val, "left": None, "right": None}

        node["left"] = left_node
        node["right"] = right_node

        queue.append((left_node, left_val, current_depth + 1))
        queue.append((right_node, right_val, current_depth + 1))

    return tree

def print_tree_dfs(tree, depth=0):
    if tree is None:
        return
    indent = "  " * depth
    print(f"{indent}- {tree['value']}")
    print_tree_dfs(tree['left'], depth + 1)
    print_tree_dfs(tree['right'], depth + 1)


tree = bin_tree_iterative(root=2, height=3)
print_tree_dfs(tree)
