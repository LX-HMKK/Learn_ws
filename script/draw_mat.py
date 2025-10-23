import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- 1. 定义齐次变换矩阵（参照 C++ 代码中的矩阵值） ---
# 注意：我们假设 C++ 代码中的 ua_T, ba_T, cu_T 都是 T_source_target 形式

# T_A^U (A in U): 假设为 C++ 中的 ua_T
T_A_U = np.array([
    [0.866, -0.5, 0, 11],
    [0.5, 0.866, 0, -1],
    [0, 0, 1, 8],
    [0, 0, 0, 1]
])

# T_A^B (A in B): 假设为 C++ 中的 ba_T
T_A_B = np.array([
    [1, 0, 0, 0],
    [0, 0.866, -0.5, 10],
    [0, 0.5, 0.866, -20],
    [0, 0, 0, 1]
])

# T_U^C (U in C): 假设为 C++ 中的 cu_T
T_U_C = np.array([
    [0.866, -0.5, 0, -3],
    [0.433, 0.75, -0.5, -3],
    [0.25, 0.433, 0.866, 3],
    [0, 0, 0, 1]
])

# --- 2. 坐标系转换和求解（参照 C++ 代码逻辑） ---
# 注意：矩阵乘法使用 np.dot() 或 @ 运算符

# C++: ca_T = cu_T * ua_T => T_A^C = T_U^C * T_A^U
T_A_C = T_U_C @ T_A_U

# C++: au_T = ua_T.inverse() => T_U^A = (T_A^U)^-1
T_U_A = np.linalg.inv(T_A_U)

# C++: ac_T = ca_T.inverse() => T_C^A = (T_A^C)^-1
T_C_A = np.linalg.inv(T_A_C)

# C++: uc_T = cu_T.inverse() => T_C^U = (T_U^C)^-1
T_C_U = np.linalg.inv(T_U_C)

# C++: bu_T = ba_T * au_T => T_U^B = T_A^B * T_U^A
T_U_B = T_A_B @ T_U_A

# 最终求解 T_C^B (C in B)

# C++: bc_T = ba_T * ac_T => T_C^B = T_A^B * T_C^A
T_C_B_1 = T_A_B @ T_C_A

# C++: bc_T = bu_T * uc_T => T_C^B = T_U^B * T_C^U
T_C_B_2 = T_U_B @ T_C_U


print("--- 坐标系变换矩阵求解 (T_C^B) ---")
print("T_C^B (Method 1: T_A^B * T_C^A):")
print(T_C_B_1.round(4))
print("\nT_C^B (Method 2: T_U^B * T_C^U):")
print(T_C_B_2.round(4))
print("\n验证两种方法的结果是否一致 (最大误差):", np.max(np.abs(T_C_B_1 - T_C_B_2)))


# --- 3. 确定相对于世界坐标系 (W=A) 的位姿，用于绘图 ---
# 假设 A 是世界坐标系 W, 即 T_A^W = I
T_W_A = np.eye(4)  # A 的位姿 (A 在 W 中)

# T_W^U = T_A^U 的逆矩阵: T_U^W = (T_A^U)^-1。这是 T_U^A 的逆。
# 我们需要 T_U^W (U 在 W 中)
T_U_W = T_U_A # T_U^A (U in A) 

# T_W^B = T_A^B 的逆矩阵: T_B^W = (T_A^B)^-1
# 我们需要 T_B^W (B in A)
T_B_W = np.linalg.inv(T_A_B)

# T_W^C = T_A^C 的逆矩阵: T_C^W = (T_A^C)^-1
# 我们需要 T_C^W (C in A)
T_C_W = T_C_A # T_C^A (C in A)

# 所有坐标系在世界坐标系 (A) 中的位姿：
Transforms = {
    'A': T_W_A,
    'U': T_U_W,
    'B': T_B_W,
    'C': T_C_W
}


# --- 4. 坐标系绘制函数 (与上一个回答中相同) ---
def plot_coordinate_system(ax, T, scale=5, label='A'):
    """
    绘制坐标系
    :param ax: Matplotlib 3D 轴对象
    :param T: 4x4 齐次变换矩阵 (T_target_source，这里是 T_source_W)
    :param scale: 坐标轴长度
    :param label: 坐标系名称
    """
    # 提取平移向量 (原点位置)
    origin = T[:3, 3]
    
    # 提取旋转矩阵 (姿态)
    R = T[:3, :3]
    
    # 经过旋转和平移后的轴向量
    x_axis = origin + R[:, 0] * scale  # X轴方向 (红色)
    y_axis = origin + R[:, 1] * scale  # Y轴方向 (绿色)
    z_axis = origin + R[:, 2] * scale  # Z轴方向 (蓝色)
    
    # 绘制坐标轴
    ax.plot([origin[0], x_axis[0]], [origin[1], x_axis[1]], [origin[2], x_axis[2]], 'r-')
    ax.plot([origin[0], y_axis[0]], [origin[1], y_axis[1]], [origin[2], y_axis[2]], 'g-')
    ax.plot([origin[0], z_axis[0]], [origin[1], z_axis[1]], [origin[2], z_axis[2]], 'b-')
    
    # 标记原点
    ax.text(origin[0], origin[1], origin[2], label, color='k', fontsize=12)


# --- 5. 初始化绘图 ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制所有坐标系
for label, T_W in Transforms.items():
    plot_coordinate_system(ax, T_W, scale=5, label=label)

# 绘制坐标系之间的连接线 (可选)
# 绘制 U -> A 的连接线 (A是世界，所以是 U 到原点)
ax.plot([Transforms['U'][:3, 3][0], Transforms['A'][:3, 3][0]],
        [Transforms['U'][:3, 3][1], Transforms['A'][:3, 3][1]],
        [Transforms['U'][:3, 3][2], Transforms['A'][:3, 3][2]], 'k:', alpha=0.5)

# 绘制 B -> A 的连接线
ax.plot([Transforms['B'][:3, 3][0], Transforms['A'][:3, 3][0]],
        [Transforms['B'][:3, 3][1], Transforms['A'][:3, 3][1]],
        [Transforms['B'][:3, 3][2], Transforms['A'][:3, 3][2]], 'k:', alpha=0.5)

# 绘制 C -> U 的连接线
ax.plot([Transforms['C'][:3, 3][0], Transforms['U'][:3, 3][0]],
        [Transforms['C'][:3, 3][1], Transforms['U'][:3, 3][1]],
        [Transforms['C'][:3, 3][2], Transforms['U'][:3, 3][2]], 'm--', alpha=0.7)


# --- 6. 设置图形属性 ---
origins = np.vstack([T[:3, 3] for T in Transforms.values()])
max_coord = np.max(origins) + 10
min_coord = np.min(origins) - 10

ax.set_xlim([min_coord, max_coord])
ax.set_ylim([min_coord, max_coord])
ax.set_zlim([min_coord, max_coord])

ax.set_xlabel('X (Red)')
ax.set_ylabel('Y (Green)')
ax.set_zlabel('Z (Blue)')
ax.set_title('Coordinate System Transformation Diagram (A, B, C, U)')
ax.view_init(elev=30, azim=-120)  # 设置初始视角

# 显示图形
plt.show()