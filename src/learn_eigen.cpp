#include "include/learn_eigen.hpp"
/*
int main() {
    Eigen::Matrix3d fixedMat;
    Eigen::MatrixXd dynamicMat(2, 3);
    
    fmt::print("Fixed Matrix rows:{},cols:{}\n", fixedMat.rows(), fixedMat.cols());
    fmt::print("Dynamic Matrix rows:{},cols:{}\n", dynamicMat.rows(), dynamicMat.cols());

    return 0;
}
*/

/*
int main() {
    Eigen::Matrix3f m;
    m<<1, 2, 3,
        4, 5, 6,
        7, 8, 9;
    // fmt::print("Matrix initialized by command:\n{}\n", m);
    std::cout << "Matrix initialized by comma:\n" << m << std::endl;
    return 0;
}
*/

int main(){
    Eigen::Matrix4f cu_T,ua_T,ca_T,ac_T,ba_T;
    ua_T<<0.866, -0.5, 0, 11,
          0.5, 0.866, 0, -1,
          0, 0, 1, 8,
          0, 0, 0, 1;

    ba_T<<1, 0, 0, 0,
          0, 0.866, -0.5, 10,
          0, 0.5, 0.866, -20,
          0, 0, 0, 1;
          
    cu_T<<0.866, -0.5, 0, -3,
          0.433, 0.75, -0.5, 3,
          0.25, 0.433, 0.866, 3,
          0, 0, 0, 1;
    
    ca_T = cu_T*ua_T;
    ac_T = ca_T.inverse();
    std::cout<<"ca_T:\n"<<ca_T<<std::endl;
    std::cout<<"\n=================================\n"<<std::endl;
    std::cout<<"ac_T:\n"<<ac_T<<std::endl;
    std::cout<<"\n=================================\n"<<std::endl;
    std::cout<<"bc_T=ba_T*ac_T:\n"<<ba_T*ac_T<<std::endl;
    return 0;
}


//特殊矩阵生成函数则能快速生成特定类型的矩阵。
//Zero()函数可生成全零矩阵，Identity()函数能生成单位矩阵，Random()函数会生成随机矩阵。
/*
int main() {
    Eigen::Matrix3d zeroMatrix = Eigen::Matrix3d::Zero();
    Eigen::Matrix3d identityMatrix = Eigen::Matrix3d::Identity();
    Eigen::Matrix3d randomMatrix = Eigen::Matrix3d::Random();
    std::cout << "Zero matrix:\n" << zeroMatrix << std::endl;
    std::cout << "Identity matrix:\n" << identityMatrix << std::endl;
    std::cout << "Random matrix:\n" << randomMatrix << std::endl;
    return 0;
}
*/

//块操作与切片技巧可用于提取矩阵的部分元素。
//例如，使用block()函数可以提取矩阵的子块：
/*
#include <iostream>
#include <Eigen/Dense>
int main() {
    Eigen::Matrix4f mat;
    mat << 1, 2, 3, 4,
            5, 6, 7, 8,
            9, 10, 11, 12,
            13, 14, 15, 16;
    //从原矩阵 mat 的第 2 行（索引 1）和第 2 列（索引 1）开始，提取一个 2×2 的子矩阵
    Eigen::Matrix2f subMat = mat.block(1, 1, 2, 2);
    std::cout << "Sub matrix:\n" << subMat << std::endl;
    return 0;
}
*/

/*
int main() {
    Eigen::Matrix2d a;
    a << 1, 2,
            3, 4;
    Eigen::Matrix2d b;
    b << 2, 3,
            1, 4;
    std::cout << "Matrix addition:\n" << a + b << std::endl;
    std::cout << "Matrix subtraction:\n" << a - b << std::endl;
    std::cout << "Element-wise multiplication:\n" << a.array() * b.array() << std::endl;
    std::cout << "Matrix multiplication:\n" << a * b << std::endl;
    return 0;
}
*/


//矩阵可通过inverse()函数计算，行列式使用determinant()函数，迹使用trace()函数
/*
int main() {
    Eigen::Matrix2d mat;
    mat << 1, 2,
            3, 4;
    std::cout << "Inverse matrix:\n" << mat.inverse() << std::endl;
    std::cout << "Determinant: " << mat.determinant() << std::endl;
    std::cout << "Trace: " << mat.trace() << std::endl;
    return 0;
}
*/


//旋转矩阵、四元数和欧拉角是描述三维空间中旋转的三种常用方式
//旋转矩阵是一个3×3的矩阵，四元数是一个四维向量，欧拉角则是三个角度的组合。

/**
 * @brief 演示如何使用 Eigen 库进行欧拉角、旋转矩阵和四元数之间的转换。
 *
 * 主要步骤如下：
 * 1. 通过欧拉角（roll, pitch, yaw）创建旋转矩阵。
 * 2. 将旋转矩阵转换为四元数。
 * 3. 从四元数获取欧拉角（yaw, pitch, roll）。
 * 4. 输出旋转矩阵、四元数和欧拉角的值。
 *
 * 该示例展示了 Eigen 库在三维空间旋转表示之间的相互转换方法。
 */
/*
int main() {
    // 从欧拉角创建旋转矩阵
    // 1. Roll (绕 X 轴旋转 M_PI / 4)
    Eigen::AngleAxisd rollAngle(M_PI / 4, Eigen::Vector3d::UnitX());
    // 2. Pitch (绕 Y 轴旋转 M_PI / 3)
    Eigen::AngleAxisd pitchAngle(M_PI / 3, Eigen::Vector3d::UnitY());
    // 3. Yaw (绕 Z 轴旋转 M_PI / 6)
    Eigen::AngleAxisd yawAngle(M_PI / 6, Eigen::Vector3d::UnitZ());
    // 4. 组合旋转 (不变)
    Eigen::Quaterniond q = yawAngle * pitchAngle * rollAngle;
    // 5. 转换为矩阵 (不变)
    Eigen::Matrix3d rotationMatrix = q.matrix();

    // 从旋转矩阵创建四元数
    Eigen::Quaterniond q2(rotationMatrix);
    // 从四元数获取欧拉角
    Eigen::Vector3d eulerAngles = q2.toRotationMatrix().eulerAngles(2, 1, 0);
    std::cout << "Rotation matrix:\n" << rotationMatrix << std::endl;
    std::cout << "Quaternion: " << q2.w() << " " << q2.x() << " " << q2.y() << " " << q2.z() << std::endl;
    std::cout << "Euler angles (yaw, pitch, roll): " << eulerAngles.transpose() << std::endl;
    return 0;
}
*/