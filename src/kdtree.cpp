#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <algorithm>
#include <queue>
#include <unordered_set> // 用于存储已处理点的索引
#include <numeric>       // for std::iota

// 自定义 Point 结构体
struct Point {
    double x;
    double y;
};

// 定义 KD-Tree 节点类
class Node {
public:
    int axis;                      // 当前分割轴
    double value;                  // 分割平面位置
    Node* left;                    // 左子树
    Node* right;                   // 右子树
    std::vector<int> point_indices; // 当前节点包含的点索引

    Node(int axis, double value, Node* left, Node* right, std::vector<int> point_indices)
        : axis(axis), value(value), left(left), right(right), point_indices(point_indices) {}
};

// 用于存储最近邻的点信息
struct Neighbor {
    double distance; // 到查询点的距离
    int index;       // 点的索引

    // 重载小于运算符，用于优先队列排序（基于距离）
    bool operator<(const Neighbor& other) const {
        return distance < other.distance;
    }
};

// 存储最近邻结果的类
class ResultSet {
public:
    int k;                                   // 最近邻数量
    std::priority_queue<Neighbor> result_set; // 最大堆存储最近邻信息
    std::unordered_set<int> visited_points; // 已处理点的索引，用于去重

    explicit ResultSet(int k) : k(k) {}

    void addPoint(double distance, int index) {
        // 如果点已经被处理，则跳过
        if (visited_points.count(index)) {
            return;
        }
        visited_points.insert(index);

        if (result_set.size() <= k) {
            result_set.emplace(Neighbor{distance, index});
        } else if (distance < result_set.top().distance) {
            result_set.pop();
            result_set.emplace(Neighbor{distance, index});
        }
    }

    double worstDist() const {
        if (result_set.empty()) {
            return std::numeric_limits<double>::infinity();
        }
        return result_set.top().distance;
    }

    void printResults(const std::vector<Point>& points) const {
        // 使用临时堆输出结果
        std::priority_queue<Neighbor> temp = result_set;
        std::unordered_set<int> printed_indices; // 用于记录已经打印的索引

        while (!temp.empty()) {
            const Neighbor& result = temp.top();
            temp.pop();

            // 检查索引是否已经打印过
            if (printed_indices.count(result.index)) {
                continue; // 跳过已经打印的索引
            }

            // 如果没有打印过，记录索引并打印
            printed_indices.insert(result.index);
            std::cout << "Point: (" << points[result.index].x << ", " << points[result.index].y
                      << "), Distance: " << result.distance << std::endl;
        }
    }
};


// 计算欧几里得距离
double calculateDistance(const Point& a, const Point& b) {
    return std::sqrt(std::pow(a.x - b.x, 2) + std::pow(a.y - b.y, 2));
}

// 递归构建 KD-Tree
Node* kdtreeRecursiveBuild(const std::vector<Point>& points,
                           const std::vector<int>& point_indices, int axis, int leaf_size) {
    if (point_indices.size() <= leaf_size) {
        return new Node(axis, 0, nullptr, nullptr, point_indices);
    }

    // 根据当前轴对点排序
    std::vector<int> sorted_indices = point_indices;
    std::sort(sorted_indices.begin(), sorted_indices.end(),
              [&](int i, int j) {
                  return axis == 0 ? points[i].x < points[j].x : points[i].y < points[j].y;
              });

    // 计算中位数
    int median_idx = sorted_indices.size() / 2;
    double median_value = axis == 0 ? points[sorted_indices[median_idx]].x : points[sorted_indices[median_idx]].y;

    // 递归构建左右子树
    Node* left = kdtreeRecursiveBuild(points, std::vector<int>(sorted_indices.begin(), sorted_indices.begin() + median_idx),
                                      (axis + 1) % 2, leaf_size);
    Node* right = kdtreeRecursiveBuild(points, std::vector<int>(sorted_indices.begin() + median_idx + 1, sorted_indices.end()),
                                       (axis + 1) % 2, leaf_size);

    return new Node(axis, median_value, left, right, {});
}

// 递归实现 k-NN 搜索
void knnSearch(Node* node, const std::vector<Point>& points, const Point& query,
               ResultSet& result_set) {
    if (!node) return;

    // 如果是叶节点，计算查询点到叶节点中每个点的距离
    if (!node->point_indices.empty()) {
        for (int idx : node->point_indices) {
            double distance = calculateDistance(points[idx], query);
            result_set.addPoint(distance, idx);
        }
        return;
    }

    // 判断查询点在分割平面哪一侧
    double query_value = node->axis == 0 ? query.x : query.y;
    Node* near_subtree = query_value <= node->value ? node->left : node->right;
    Node* far_subtree = query_value <= node->value ? node->right : node->left;

    // 优先搜索与查询点同侧的子树
    knnSearch(near_subtree, points, query, result_set);

    // 检查是否需要搜索另一侧子树
    double distance_to_plane = std::abs(query_value - node->value);
    if (distance_to_plane < result_set.worstDist()) {
        knnSearch(far_subtree, points, query, result_set);
    }
}

int main() {
    // 示例点
    std::vector<Point> points = {{2, 3}, {5, 4}, {9, 6}, {4, 7}, {8, 1}, {7, 2}, {6, 3}, {1, 9}, {3, 8}};
    std::vector<int> point_indices(points.size());
    std::iota(point_indices.begin(), point_indices.end(), 0); // 填充索引 [0, 1, 2, ...]

    // 构建 KD-Tree
    Node* kd_tree = kdtreeRecursiveBuild(points, point_indices, 0, 1);

    // 查询点
    Point query_point = {6, 4};

    // 执行 k-NN 搜索
    int k = 3;
    ResultSet result_set(k);
    knnSearch(kd_tree, points, query_point, result_set);

    // 输出结果
    std::cout << "Query Point: (" << query_point.x << ", " << query_point.y << ")" << std::endl;
    std::cout << "Nearest Neighbors:" << std::endl;
    result_set.printResults(points);

    return 0;
}
