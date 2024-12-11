import matplotlib.pyplot as plt

class Node:
    """
    KD-Tree 节点类
    """
    def __init__(self, axis=None, value=None, left=None, right=None, point_indices=None):
        self.axis = axis  # 当前分割轴
        self.value = value  # 分割平面位置
        self.left = left  # 左子树
        self.right = right  # 右子树
        self.point_indices = point_indices  # 当前节点包含的点

def axis_round_robin(axis, dim):
    """
    轮转选择分割轴
    """
    return (axis + 1) % dim

def sort_key_by_value(point_indices, points, axis):
    """
    根据某个轴的值对点进行排序
    """
    return sorted(point_indices, key=lambda idx: points[idx][axis])

def kdtree_recursive_build(points, point_indices, axis=0, leaf_size=1, plot_range=None, ax=None):
    """
    递归构建 KD-Tree，并包含可视化功能。
    """
    if len(point_indices) <= leaf_size:
        # 创建叶节点，存储点索引
        return Node(axis=axis, value=None, left=None, right=None, point_indices=point_indices)

    # 根据分割轴排序
    point_indices_sorted = sort_key_by_value(point_indices, points, axis)

    # 计算分割线的位置（不是点的坐标，而是点范围的中间值）
    min_value = min(points[idx][axis] for idx in point_indices_sorted)
    max_value = max(points[idx][axis] for idx in point_indices_sorted)
    median_value = (min_value + max_value) / 2+0.2  # 取中间值作为分割线

    # 可视化分割
    draw_partition(points, point_indices_sorted, axis, median_value, plot_range, ax)

    # 更新绘图范围
    new_plot_range = update_plot_range(plot_range, axis, median_value)

    # 递归构造左右子树
    left_child = kdtree_recursive_build(
        points, [idx for idx in point_indices_sorted if points[idx][axis] <= median_value],
        axis_round_robin(axis, len(points[0])), leaf_size, new_plot_range['left'], ax)
    right_child = kdtree_recursive_build(
        points, [idx for idx in point_indices_sorted if points[idx][axis] > median_value],
        axis_round_robin(axis, len(points[0])), leaf_size, new_plot_range['right'], ax)

    # 创建当前节点，存储分割轴、分割值、左右子树
    return Node(axis=axis, value=median_value, left=left_child, right=right_child, point_indices=point_indices)

def draw_partition(points, point_indices, axis, value, plot_range, ax):
    """
    绘制分割平面和点
    """
    x_coords = [points[idx][0] for idx in point_indices]
    y_coords = [points[idx][1] for idx in point_indices]

    # 获取当前区域范围
    x_min, x_max, y_min, y_max = plot_range

    # 绘制点
    ax.scatter(x_coords, y_coords, color='blue')

    # 绘制分割线，覆盖整个子区域
    if axis == 0:  # x轴分割
        ax.plot([value, value], [y_min, y_max], 'r--', label=f"x={value}")
    else:  # y轴分割
        ax.plot([x_min, x_max], [value, value], 'g--', label=f"y={value}")

    plt.pause(1)

def update_plot_range(plot_range, axis, value):
    """
    更新绘图范围
    :param plot_range: 当前范围 (x_min, x_max, y_min, y_max)
    :param axis: 当前分割轴
    :param value: 分割平面位置
    :return: 左子树和右子树的范围
    """
    if plot_range is None:
        plot_range = [0, 10, 0, 10]

    if axis == 0:  # x轴分割
        return {
            'left': [plot_range[0], value, plot_range[2], plot_range[3]],
            'right': [value, plot_range[1], plot_range[2], plot_range[3]]
        }
    else:  # y轴分割
        return {
            'left': [plot_range[0], plot_range[1], plot_range[2], value],
            'right': [plot_range[0], plot_range[1], value, plot_range[3]]
        }

def print_kd_tree(node, points, depth=0):
    """
    打印 KD-Tree 的结构
    """
    if node is None:
        return

    indent = "  " * depth
    if node.value is None:
        print(f"{indent}Leaf Node: Points {[points[idx] for idx in node.point_indices]}")
    else:
        print(f"{indent}Depth {depth}, Axis {node.axis}, Split at {node.value}")

    print_kd_tree(node.left, points, depth + 1)
    print_kd_tree(node.right, points, depth + 1)

# 示例点
points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (6, 3), (1, 9), (3, 8)]
point_indices = list(range(len(points)))

# 设置绘图
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title("KD-Tree Construction Visualization")
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel("x")
ax.set_ylabel("y")

# 构建 KD-Tree
kd_tree = kdtree_recursive_build(points, point_indices, plot_range=[0, 10, 0, 10], ax=ax)

# 显示最终分割
plt.show()

# 打印 KD-Tree 结构
print_kd_tree(kd_tree, points)
