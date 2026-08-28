# Titanic 数据分析 Notebook

用 pandas 分析 Kaggle 经典 Titanic 数据集，覆盖缺失值、分布、相关性、分组聚合与讲故事的图 5 项分析。

## 环境
- Python 3.13（托管版）隔离 venv，依赖：pandas / matplotlib / seaborn / jupyter
- 重新创建环境：`python -m venv .venv` 后 `.\.venv\Scripts\python.exe -m pip install pandas matplotlib seaborn jupyter nbformat nbconvert ipykernel`

## 运行
```bash
# 1) 启动 Jupyter 交互查看（已执行，含输出）
.\.venv\Scripts\python.exe -m jupyter notebook titanic_analysis.ipynb

# 2) 重新执行并写回输出
.\.venv\Scripts\python.exe -m jupyter nbconvert --execute --to notebook --inplace titanic_analysis.ipynb
```

## 文件
- `titanic_analysis.ipynb` —— 分析报告（主交付物）
- `data/titanic.csv` —— 数据集
- `build_notebook.py` —— 用 nbformat 拼装 Notebook 的脚本（便于复现）
- `overview.md` —— 交付概览
