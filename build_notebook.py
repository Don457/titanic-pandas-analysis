"""生成 Titanic 数据分析 Jupyter Notebook（含 5 项分析）。

用法：
    python build_notebook.py          # 生成 titanic_analysis.ipynb
    jupyter nbconvert --execute --to notebook --inplace titanic_analysis.ipynb  # 执行并嵌入输出

说明：本脚本仅负责"拼装" Notebook 结构，真正的数据分析代码写在下面的 code 单元格里，
由 nbconvert 在隔离 venv 中实际执行，确保所见即所得。
"""
from __future__ import annotations

import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

cells: list = []

# ----------------------------------------------------------------------------
# 0. 封面 / 说明
# ----------------------------------------------------------------------------
cells.append(new_markdown_cell(
    "# Titanic 生存数据分析报告\n\n"
    "**数据集**：Titanic（Kaggle 经典公开数据集，891 名乘客，12 个字段）\n\n"
    "**分析目标（5 项）**：\n"
    "1. 缺失值统计：各列缺失数量与比例\n"
    "2. 分布直方图：关键数值列的分布\n"
    "3. 相关性热力图：数值列间的相关系数\n"
    "4. 分组聚合：`groupby` 与 `pivot_table` 做聚合统计\n"
    "5. 讲故事的图：一张能清晰传达洞察的可视化\n\n"
    "**技术栈**：`pandas`（读取/聚合）、`matplotlib` + `seaborn`（绘图）。\n"
    "涉及基础操作：`read_csv`、`groupby`、`merge`、`pivot_table`。"
))

# ----------------------------------------------------------------------------
# 1. 导入与读取
# ----------------------------------------------------------------------------
cells.append(new_markdown_cell(
    "## 0. 导入库并读取数据\n\n"
    "使用 `pandas.read_csv` 载入 CSV，并快速预览数据结构与数值概览。"
))
cells.append(new_code_cell(
    "# ---- 导入常用库 ----\n"
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n"
    "\n"
    "%matplotlib inline\n"
    "sns.set_theme(style='whitegrid')\n"
    "plt.rcParams['figure.dpi'] = 110\n"
    "\n"
    "# read_csv：从本地 CSV 读取为 DataFrame（这是 pandas 最基础的读取操作）\n"
    "df = pd.read_csv('data/titanic.csv')\n"
    "\n"
    "# 整体规模与数值概览：shape 看行/列，describe 看数值列统计\n"
    "print(f'数据形状: {df.shape}')\n"
    "print(f'整体生存率: {df[\"Survived\"].mean():.3f}')\n"
    "display(df.head())\n"
    "display(df.describe().round(2))"
))

# ----------------------------------------------------------------------------
# 2. 分析 1：缺失值统计
# ----------------------------------------------------------------------------
cells.append(new_markdown_cell(
    "## 1. 缺失值统计\n\n"
    "统计每一列的缺失值**数量**与**比例**，定位需要清洗或谨慎使用的字段。"
))
cells.append(new_code_cell(
    "# isnull().sum() 统计每列缺失数量；除以总行数得到缺失比例\n"
    "missing_count = df.isnull().sum()\n"
    "missing_ratio = missing_count / len(df)\n"
    "\n"
    "# 合并为一张整洁的汇总表（只用基础操作，不引入新依赖）\n"
    "missing_tbl = pd.DataFrame({\n"
    "    'missing_count': missing_count,\n"
    "    'missing_ratio': missing_ratio.round(4),\n"
    "}).sort_values('missing_count', ascending=False)\n"
    "\n"
    "print('=== 缺失值统计 ===')\n"
    "missing_tbl"
))

# ----------------------------------------------------------------------------
# 3. 分析 2：分布直方图
# ----------------------------------------------------------------------------
cells.append(new_markdown_cell(
    "## 2. 分布直方图\n\n"
    "对关键数值列（`Age`、`Fare`、`SibSp`、`Parch`）绘制分布直方图，"
    "直观感受乘客年龄、票价与同行亲属数量的分布形态。"
))
cells.append(new_code_cell(
    "# 用 2x2 子图一次性展示四个数值列的分布\n"
    "num_cols = ['Age', 'Fare', 'SibSp', 'Parch']\n"
    "fig, axes = plt.subplots(2, 2, figsize=(11, 7))\n"
    "for ax, col in zip(axes.ravel(), num_cols):\n"
    "    # dropna 避免 NaN 干扰直方图计数\n"
    "    ax.hist(df[col].dropna(), bins=30, color='#4C72B0', edgecolor='white')\n"
    "    ax.set_title(f'Distribution of {col}')\n"
    "    ax.set_xlabel(col)\n"
    "    ax.set_ylabel('count')\n"
    "fig.suptitle('Key Numerical Columns Distribution', fontsize=14)\n"
    "fig.tight_layout()\n"
    "plt.show()"
))

# ----------------------------------------------------------------------------
# 4. 分析 3：相关性热力图
# ----------------------------------------------------------------------------
cells.append(new_markdown_cell(
    "## 3. 相关性热力图\n\n"
    "对数值列计算 Pearson 相关系数矩阵，并用 `seaborn.heatmap` 可视化，"
    "快速发现哪些变量彼此相关（例如 `Fare` 与 `Pclass` 负相关）。"
))
cells.append(new_code_cell(
    "# corr：仅对数值列计算相关系数（numeric_only 过滤掉文本列）\n"
    "corr = df.corr(numeric_only=True)\n"
    "fig, ax = plt.subplots(figsize=(8, 6))\n"
    "sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',\n"
    "            square=True, linewidths=.5, ax=ax)\n"
    "ax.set_title('Correlation Heatmap (numerical columns)')\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

# ----------------------------------------------------------------------------
# 5. 分析 4：分组聚合（groupby + merge + pivot_table）
# ----------------------------------------------------------------------------
cells.append(new_markdown_cell(
    "## 4. 分组聚合\n\n"
    "- 用 `merge` 把 `Pclass` 代码（1/2/3）映射为可读性更好的类名；\n"
    "- 用 `groupby` 按 `Pclass` / `Sex` 做聚合统计；\n"
    "- 用 `pivot_table` 生成「性别 × 舱位」的生存率矩阵。"
))
cells.append(new_code_cell(
    "# merge：把舱位代码映射为类名（演示 merge 基础操作，how='left' 保留原表）\n"
    "class_map = pd.DataFrame({\n"
    "    'Pclass': [1, 2, 3],\n"
    "    'ClassName': ['First', 'Second', 'Third'],\n"
    "})\n"
    "df = df.merge(class_map, on='Pclass', how='left')\n"
    "\n"
    "# groupby ①：按舱位聚合（平均票价、平均年龄、生存率、人数）\n"
    "by_class = df.groupby('ClassName').agg(\n"
    "    avg_fare=('Fare', 'mean'),\n"
    "    avg_age=('Age', 'mean'),\n"
    "    survival_rate=('Survived', 'mean'),\n"
    "    n=('Survived', 'size'),\n"
    ").round(3)\n"
    "print('=== 按舱位分组聚合 ===')\n"
    "display(by_class)\n"
    "\n"
    "# groupby ②：按性别看整体生存率（与舱位结果互为补充）\n"
    "by_sex = df.groupby('Sex')['Survived'].agg(['mean', 'size']).round(3)\n"
    "print('=== 按性别分组聚合 ===')\n"
    "display(by_sex)\n"
    "\n"
    "# groupby ③：先按年龄分箱（pd.cut），再 groupby 看各年龄段生存率\n"
    "df['AgeBand'] = pd.cut(\n"
    "    df['Age'],\n"
    "    bins=[0, 12, 18, 35, 60, 100],\n"
    "    labels=['Child', 'Teen', 'Adult', 'Senior', 'Elder'],\n"
    ")\n"
    "by_age = df.groupby('AgeBand', observed=True)['Survived'].agg(['mean', 'size']).round(3)\n"
    "print('=== 按年龄段分组聚合 ===')\n"
    "display(by_age)\n"
    "\n"
    "# groupby ④：按登船港口（Embarked）看生存率\n"
    "by_embark = df.groupby('Embarked')['Survived'].agg(['mean', 'size']).round(3)\n"
    "print('=== 按登船港口分组聚合 ===')\n"
    "display(by_embark)\n"
    "\n"
    "# pivot_table：行=性别，列=舱位，值=生存率，得到交叉汇总矩阵\n"
    "surv_pivot = pd.pivot_table(\n"
    "    df, index='Sex', columns='ClassName',\n"
    "    values='Survived', aggfunc='mean',\n"
    ").round(3)\n"
    "print('=== 性别 × 舱位 生存率矩阵 ===')\n"
    "surv_pivot"
))

# ----------------------------------------------------------------------------
# 6. 分析 5：讲故事的图
# ----------------------------------------------------------------------------
cells.append(new_markdown_cell(
    "## 5. 讲故事的图：谁更可能活下来？\n\n"
    "把上面的 `pivot_table` 直接画成「分组柱状图」：x 轴为性别，颜色区分舱位，y 轴是生存率。\n\n"
    "**洞察**：无论哪个舱位，女性生存率都显著高于男性；且头等舱生存率整体最高——"
    "这正是 Titanic 事件中「妇女与儿童优先（尤其一等舱）」历史的量化体现。"
))
cells.append(new_code_cell(
    "# 用 pivot_table 的结果绘图，让数据自己讲故事\n"
    "fig, ax = plt.subplots(figsize=(9, 5.5))\n"
    "surv_pivot.plot(kind='bar', ax=ax, color=['#55A868', '#4C72B0', '#C44E52'])\n"
    "ax.set_title('Survival Rate by Sex and Passenger Class', fontsize=14)\n"
    "ax.set_xlabel('Sex')\n"
    "ax.set_ylabel('Survival Rate')\n"
    "ax.set_ylim(0, 1.05)\n"
    "ax.legend(title='Class')\n"
    "\n"
    "# 在柱顶标注具体数值，便于阅读（bar_label 是 matplotlib 新版本特性）\n"
    "for container in ax.containers:\n"
    "    ax.bar_label(container, fmt='%.2f', label_type='edge', padding=2)\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

# ----------------------------------------------------------------------------
# 7. 结论
# ----------------------------------------------------------------------------
cells.append(new_markdown_cell(
    "## 结论小结\n\n"
    "- **缺失值**：`Cabin` 缺失最严重（约 77%），`Age` 约 20% 缺失，建模时需处理；"
    "`Embarked` 仅 2 条缺失可简单填充。\n"
    "- **分布**：票价 `Fare` 右偏严重（多数人低票价，少数极高），`Age` 集中在 20–40 岁。\n"
    "- **相关性**：`Fare` 与 `Survived` 正相关、`Pclass` 与 `Survived` 负相关——"
    "有钱/高舱位更易幸存。\n"
    "- **分组聚合**：头等舱生存率最高；女性生存率是男性的数倍。\n"
    "- **故事图**：性别 + 舱位共同决定了生存机会，一等舱女性生存率接近 0.97。\n\n"
    "> 进阶方向：用 `fillna` 处理 `Age`/`Embarked`、对 `Fare` 做 log 变换、"
    "用 `sklearn` 训练一个生存预测模型。"
))

nb = new_notebook(cells=cells)
nb.metadata['kernelspec'] = {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}
nb.metadata['language_info'] = {'name': 'python'}

with open('titanic_analysis.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print('Notebook 已生成: titanic_analysis.ipynb')
print(f'单元格总数: {len(cells)}')
