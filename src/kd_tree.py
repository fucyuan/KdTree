# import matplotlib.pyplot as plt

# class KDNode:
#     """
#     KD-Tree 节点类
#     """
#     def __init__(self, point=None, axis=None, left=None, right=None):
#         self.point = point  # 当前节点存储的点 (x, y)
#         self.axis = axis    # 当前分割的轴 (0: x轴, 1: y轴)
#         self.left = left    # 左子树
#         self.right = right  # 右子树
 
# def build_kd_tree(points, depth=0):
#     """
#     构建 KD-Tree
#     :param points: 二维点的列表 [(x1, y1), (x2, y2), ...]
#     :param depth: 当前深度，用于选择分割轴
#     :return: KDNode 树的根节点
#     """
#     if not points:
#         return None

#     # 根据深度选择分割轴 (0 为 x 轴，1 为 y 轴)
#     axis = depth % 2

#     # 按照当前轴排序并选择中位数作为根节点
#     points.sort(key=lambda point: point[axis])
#     median = len(points) // 2

#     # 绘制分割过程
#     draw_partition(points, axis, depth)

#     # 递归构造左子树和右子树
#     return KDNode(
#         point=points[median],
#         axis=axis,
#         left=build_kd_tree(points[:median], depth + 1),
#         right=build_kd_tree(points[median + 1:], depth + 1)
#     )

# def draw_partition(points, axis, depth):
#     """
#     绘制分割平面和点
#     :param points: 当前的点列表
#     :param axis: 分割轴 (0: x轴, 1: y轴)
#     :param depth: 当前深度
#     """
#     x_coords = [p[0] for p in points]
#     y_coords = [p[1] for p in points]

#     # 绘制点
#     plt.scatter(x_coords, y_coords, label=f"Depth {depth}")

#     # 绘制分割线
#     median_index = len(points) // 2
#     if axis == 0:  # x轴分割
#         plt.axvline(x=points[median_index][0], color='red', linestyle='--', label=f"Split x={points[median_index][0]}")
#     else:  # y轴分割
#         plt.axhline(y=points[median_index][1], color='blue', linestyle='--', label=f"Split y={points[median_index][1]}")

#     # 图例
#     plt.legend()
#     plt.pause(1)  # 暂停显示分割过程

# def print_kd_tree(node, depth=0):
#     """
#     打印 KD-Tree 的结构
#     :param node: 当前节点
#     :param depth: 当前深度
#     """
#     if node is None:
#         return
#     print(" " * depth * 2, f"Depth {depth}, Axis {node.axis}, Point {node.point}")
#     print_kd_tree(node.left, depth + 1)
#     print_kd_tree(node.right, depth + 1)

# # 示例点
# points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]

# # 设置绘图
# plt.figure(figsize=(8, 8))
# plt.title("KD-Tree Construction Visualization")
# plt.xlabel("x")
# plt.ylabel("y")

# # 构建 KD-Tree
# kd_tree = build_kd_tree(points)

# # 显示最终分割
# plt.show()

# # 打印 KD-Tree 结构
# print_kd_tree(kd_tree)
import matplotlib.pyplot as plt

class KDNode:
    """
    KD-Tree 节点类
    """
    def __init__(self, point=None, axis=None, left=None, right=None):
        self.point = point  # 当前节点存储的点 (x, y)
        self.axis = axis    # 当前分割的轴 (0: x轴, 1: y轴)
        self.left = left    # 左子树
        self.right = right  # 右子树

def build_kd_tree(points, depth=0, plot_range=None, ax=None):
    """
    构建 KD-Tree
    :param points: 二维点的列表 [(x1, y1), (x2, y2), ...]
    :param depth: 当前深度，用于选择分割轴
    :param plot_range: 当前绘图范围 (x_min, x_max, y_min, y_max)
    :param ax: matplotlib 轴对象，用于绘制
    :return: KDNode 树的根节点
    """
    if not points:
        return None

    # 根据深度选择分割轴 (0 为 x 轴，1 为 y 轴)
    axis = depth % 2

    # 按照当前轴排序并选择中位数作为根节点
    points.sort(key=lambda point: point[axis])
    median = len(points) // 2
    point = points[median]

    # 可视化分割
    draw_partition(points, point, axis, plot_range, ax)

    # 更新绘图范围
    new_plot_range = update_plot_range(plot_range, axis, point)

    # 递归构造左子树和右子树
    left = build_kd_tree(points[:median], depth + 1, new_plot_range['left'], ax)
    right = build_kd_tree(points[median + 1:], depth + 1, new_plot_range['right'], ax)

    return KDNode(point=point, axis=axis, left=left, right=right)

def draw_partition(points, point, axis, plot_range, ax):
    """
    绘制分割平面和点
    :param points: 当前的点列表
    :param point: 中位点 (x, y)
    :param axis: 分割轴 (0: x轴, 1: y轴)
    :param plot_range: 当前绘图范围 (x_min, x_max, y_min, y_max)
    :param ax: matplotlib 的轴对象
    """
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
     # 初始化 plot_range 的默认值
    if plot_range is None:
        plot_range = [0, 10, 0, 10]  # 假设绘图范围为 [0, 10] x [0, 10]

    # 绘制点
    ax.scatter(x_coords, y_coords, color='blue')

    # 绘制分割线
    if axis == 0:  # x轴分割
        ax.plot([point[0], point[0]], [plot_range[2], plot_range[3]], 'r--')
    else:  # y轴分割
        ax.plot([plot_range[0], plot_range[1]], [point[1], point[1]], 'g--')
    plt.legend()
    plt.pause(1)  # 暂停显示分割过程

def update_plot_range(plot_range, axis, point):
    """
    更新绘图范围
    :param plot_range: 当前范围 (x_min, x_max, y_min, y_max)
    :param axis: 当前分割轴
    :param point: 中位点 (x, y)
    :return: 左子树和右子树的范围
    """
    if plot_range is None:
        plot_range = [0, 10, 0, 10]

    if axis == 0:  # x轴分割
        return {
            'left': [plot_range[0], point[0], plot_range[2], plot_range[3]],
            'right': [point[0], plot_range[1], plot_range[2], plot_range[3]]
        }
    else:  # y轴分割
        return {
            'left': [plot_range[0], plot_range[1], plot_range[2], point[1]],
            'right': [plot_range[0], plot_range[1], point[1], plot_range[3]]
        }

def print_kd_tree(node, depth=0):
    """
    打印 KD-Tree 的结构
    :param node: 当前节点
    :param depth: 当前深度
    """
    if node is None:
        return
    print(" " * depth * 2, f"Depth {depth}, Axis {node.axis}, Point {node.point}")
    print_kd_tree(node.left, depth + 1)
    print_kd_tree(node.right, depth + 1)

# 示例点
points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]

# 设置绘图
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title("KD-Tree Construction Visualization")
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel("x")
ax.set_ylabel("y")

# 构建 KD-Tree
kd_tree = build_kd_tree(points, ax=ax)

# 显示最终分割
plt.show()

# 打印 KD-Tree 结构
print_kd_tree(kd_tree)

