# 实验复现简易教程

本项目已完成医疗数据治理、弱标注实验及结果验证，按以下步骤可完全复现报告中的结果。

## 1. 环境准备
确保已安装以下 Python 库：
- `pandas`
- `numpy`

## 2. 复现步骤

### 第一步：数据问题诊断
生成缺失值分析、标签噪音画像及子群体风险分布的证据。
```powershell
python scripts/diagnose/advanced_diagnose.py
```

### 第二步：运行 LF 迭代实验
对比 Majority Vote 与加权 Label Model 在覆盖率和准确率上的权衡。
```powershell
python scripts/experiments/label_model_experiment.py
```

### 第三步：生成最终结果 (Test Set)
对 240 条测试数据进行推理，产出最终提交文件。
```powershell
python scripts/experiments/final_eval.py
```

## 3. 产出物说明
执行完成后，您可以在以下路径查看结果：
- `results/predictions.csv`: 测试集预测结果。
- `results/evaluation_results.txt`: 最终指标日志。
- `final_report.md`: 完整的实验分析报告。
