def bin_tree_recursive(root=2, height=6):

    if height == 0:
        return None

    left = root * 3
    right = root + 4

    return {
        "value": root,
        "left": bin_tree_recursive(left, height - 1),
        "right": bin_tree_recursive(right, height - 1),
    }

