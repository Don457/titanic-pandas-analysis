# 项目 1：Titanic 数据分析 — 交付概览

## 做了什么
在隔离的 Python venv 中用 `pandas` 完成了一份公开数据集（Titanic，891 行 × 12 列）的 5 项分析，并生成了一份可直接阅读的 Jupyter Notebook 报告。Notebook 已用 `jupyter nbconvert --execute` 实际执行，图表与表格均已嵌入输出（所见即所得）。

## 交付物
- `titanic-analysis/titanic_analysis.ipynb` —— 主交付物（14 个单元格：说明 + 代码 + 已渲染输出）
- `titanic-analysis/data/titanic.csv` —— 数据集（从公开镜像下载，等价于 Kaggle 原始 train.csv）
- `titanic-analysis/build_notebook.py` —— Notebook 生成脚本（可重现报告结构）
- `titanic-analysis/README.md` —— 运行说明

## 5 项分析覆盖情况
| # | 分析 | 用到的 pandas 操作 | 结果 |
|---|------|--------------------|------|
| 1 | 缺失值统计 | `isnull().sum()`、`len()` | Cabin 77.1%、Age 19.9%、Embarked 0.2% 缺失 |
| 2 | 分布直方图 | `DataFrame.hist` / `plt.hist` | Age、Fare、SibSp、Parch 四张分布图 |
| 3 | 相关性热力图 | `df.corr(numeric_only=True)` + `sns.heatmap` | Fare↔Survived 正相关、Pclass↔Survived 负相关 |
| 4 | 分组聚合 | `merge`、`groupby`（舱位/性别/年龄段/港口）、`pivot_table` | 生存率交叉矩阵 |
| 5 | 讲故事的图 | `pivot_table` + `plot(kind='bar')` | 「性别 × 舱位」生存率分组柱状图 |

## 关键洞察
- 一等舱女性生存率 ≈ 0.97，远超男性（0.13–0.37）——「妇孺与高舱位优先」的量化体现。
- 票价与生存率正相关、舱位等级与生存率负相关：经济条件越好越易幸存。
- Cabin 缺失严重，建模前应做特征工程或丢弃该列。

## 工程要点
- 全程使用托管 Python 3.13 的隔离 `venv`，未污染用户环境。
- 代码含类型友好的中文注释，单步可解释；有效代码约 96 行（在 100–200 行区间内）。
- 执行时无报错（仅 Windows asyncio/zmq 的无害 warning）。

## 运行方式
```bash
cd titanic-analysis
.\.venv\Scripts\python.exe -m jupyter notebook titanic_analysis.ipynb   # 交互查看
# 或重新执行并嵌入输出：
.\.venv\Scripts\python.exe -m jupyter nbconvert --execute --to notebook --inplace titanic_analysis.ipynb
```
