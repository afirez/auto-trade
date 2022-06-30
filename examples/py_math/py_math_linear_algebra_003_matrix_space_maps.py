
'''
1 矩阵的核心（下）：空间映射

利用矩阵表示空间映射
回顾上一讲中所讲的内容，在默认基底 
(e1,e2,...,en) 构成的 Rn
 空间中，矩阵 A 与列向量 x 的乘法 Ax 的本质就是变换向量的基底。将默认基底中的各基向量 
(e1,e2,...,en)
 分别对应的变换为矩阵 A 的各列，由矩阵 A 的各列充当新的“基向量”，
 再结合原向量的坐标，得到目标向量在目标空间中的新位置。

总结概况一下：由于矩阵乘法的作用，原始向量的空间位置甚至其所在空间的维度和形态都发生了改变，
  这便是矩阵乘法的空间映射作用。

我们要着重强调一下：在第一段中，我们将基向量打了引号，原因是这种说法并不完全准确。
  因为我们在上一讲的结尾曾经提到：矩阵 A 的各列向量作为向量 x 默认基底经过转换后的目标向量，
  由于其在维度和线性相关性方面存在各种不同的情况，
  因此这组目标向量的张成空间和原始向量所在的空间之间，就会存在多种不同的对应关系。
'''

'''
2 矮胖矩阵对空间的降维压缩

当 m<n 的时候，矩阵是一个外表“矮胖“的矩阵，向量 x 是 Rn
 空间中的一个 n 维向量，x 的 n 个基向量 ei
 分别被矩阵 A 映射成了 n 个 m 维向量，
 由于 m<n，这一组目标向量所能张成的空间维数最大就是 m。
 这样一来，在矩阵 A 的作用下，位于 Rn
 空间中的任意向量 x，经过映射作用，都转换到了一个维数更低的新空间中的新位置。
 由此我们看出，“矮胖”矩阵 A 压缩了原始空间 Rn。

 3 个二维向量线性相关，张成空间的问题, 分两种情况。

第一种情况是：

如果这 3 个二维目标向量共面但不共线，那么其所有的线性组合结果就构成二维平面 R2
，经过矩阵 A 的映射，整个向量空间就被压缩成了二维

第二种情况：

如果这 3 个二维向量共线，那么其线性组合就只能分布在二维平面 R2
 中的一条过原点 (0,0) 的直线上，经过矩阵的映射，整个向量空间被压缩成了一维
'''

'''
3 高瘦矩阵无法覆盖目标空间

原理：向量信息不增加

现在我们来看看另一种形态的矩阵，即 m×n 矩阵中的 m>n 这种情况，我们称之为“高瘦”矩阵。

x 的 n 个基向量 ei
 分别被矩阵 A 映射成了 n 个 m 维向量，
 由于 m>n，看上去 x 映射后的目标向量的维数提高了，变成了 m 维。
 那我们能不能说：经过矩阵 A 的映射，原始向量 x 构成的空间 Rn
 变成了维数更高的空间 Rm
 呢？答案是否定的，哲学点说，一个事物无中生有，那是不可能的，平白无故地一个向量携带的信息怎么能增加呢?

 2 个三维向量，张成空间的问题, 分两种情况。

第一种情况是：

两个向量线性无关，那么张成空间就是一个二维平面，
这里需要注意一下，这个二维平面不是一个前面见过的由 x 轴和 y 轴构成的 R2 平面，
而是一个“斜搭”在三维空间中的二维平面，
构成平面的每一个点都是三维的，
而这个二维平面的具体形态，
则和这两个三维向量的具体值选取密切相关。

我们再讨论第二种情况：

如果两个向量线性相关，那么张成空间就是一条直线，
那么同样地，这个直线是经过零点，并“斜穿”过三维空间 R3 的一条直线
'''

'''
4 分多种情况的方阵映射

至于说如果矩阵 A 是一个 n 阶方阵，
分析方法也是一样的，核心问题仍然是分析 A 的各列向量的线性相关性，
我们很容易发现，Rn 空间中的向量经过矩阵 A 的映射，
其目标空间的维度就是这 n 个 n 维列向量的张成空间的维度，
其映射空间的维度必然小于等于 n。

当矩阵 A 的三个列向量线性无关的时候，
意味着原始向量 x 的基经过映射后的目标向量仍然可以构成三维空间 R3 的一组基。
这是非常好的一种情况，意味着原始空间 R3 经过矩阵 A 的映射，
其映射后得到的空间仍然是等维的 R3 空间。
原始向量空间在这个过程中没有被压缩，
并且映射后空间内的每一个向量也都能找到对应的原始向量。
这种一一映射的关系我们在后面讲逆映射、逆矩阵的时候还会反复讨论，这里先有一个整体印象就好。

而当 A 的三个列向量线性相关的时候，其实就退化成“高瘦”矩阵里所讨论的情况了，
由于之前详细用图分析过具体情形，我们这里就只需要简单的说明结论，相信大家很容易理解。

情况一：当这三个列向量共面但不共线的时候，
 R3 空间中的向量经过映射，最后分布在“搭”在三维空间 R3 中的一个平面上。

情况二：当这三个列向量共线的时候，
 R3 空间中的向量经过映射，最后分布在“穿”过三维空间 R3 中的一条直线上。
'''

'''
空间映射形态的决定因素

矩阵的秩

这一讲里，我们举了这么多例子，画了这么多的图，是时候来提炼一些东西了，
我们把一个空间经过矩阵映射后得到的新空间称之为它的像空间。
我们发现，一个原始空间，经过几个形状相同的矩阵进行映射，像空间的维数可能不同；
经过几个不同形状的矩阵进行映射，又有可能得到维数相同的像空间。那么决定因素是什么？

决定因素就是空间映射矩阵的列向量，
列向量张成空间的维数就是原始空间映射后的像空间维数。
我们给矩阵列向量的张成空间维数取了一个名字，就叫作：矩阵的秩。
从另一方面看，秩也可以说是该矩阵线性无关的列的个数。
'''

'''
用 Python 求解矩阵的秩
'''

import numpy as np

A_1 = np.array([[1, 1, 0],
              [1, 0, 1]])

A_2 = np.array([[1, 2, -1],
              [2, 4, -2]])

A_3 = np.array([[1, 0],
              [0, 1],
              [0, -1]])

A_4 = np.array([[1, 2],
              [1, 2],
              [-1, -2]])

A_5 = np.array([[1, 1, 1],
              [1, 1, 2],
              [1, 2, 3]])

print(np.linalg.matrix_rank(A_1))
print(np.linalg.matrix_rank(A_2))
print(np.linalg.matrix_rank(A_3))
print(np.linalg.matrix_rank(A_4))
print(np.linalg.matrix_rank(A_5))