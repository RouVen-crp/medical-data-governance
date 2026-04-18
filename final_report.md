# 医疗数据治理与弱标注作业报告

## 1. 项目概览与数据特征

根据 `@互评作业1/data/manifest.json` 统计，本项目处理的合成数据集规模如下：
- **全量样本**: 训练集 (5000)、验证集 (120)、测试集 (240)。
- **科室分布**: 全科 (GeneralMedicine, 7374) 占比最高，急诊科 (Emergency, 179) 样本最稀缺。
- **标签平衡**: 干净标签分布为 0: 7949, 1: 4412。

---

## 2. 循证数据问题诊断 (Evidence-based Diagnosis)

通过执行 `scripts/diagnose/advanced_diagnose.py`，识别出以下核心治理问题：

### 2.1 缺失机制分析
- **lab_abnormal_count**: 缺失率较低 (~3%)，在急诊科最低 (1.25%)，符合急诊指标必填的业务逻辑。
- **length_of_stay_proxy**: 在心内科 (Cardiology) 缺失率最高 (21%)，呈现明显的 **MAR (Missing at Random)** 特征。

### 2.2 标签噪音画像
对比 `risk_label_noisy` 与 `risk_label_clean`：
- **False Positives (FP)**: 极大部分虚报集中在 **GeneralMedicine**，历史标签对全科常规病例（如常规随访、开药）存在过度判定。
- **False Negatives (FN)**: 漏报主要集中在 **Cardiology**，历史标签漏掉了关键的心内科高危信号。

### 2.3 时间漂移
- 真实风险率从 2024Q2 的 **25.9%** 升至 2024Q4 的 **58.0%**，表明后期季度判定门槛或患者严重程度发生了漂移。

---

## 3. 弱监督规则 (LFs) 设计与迭代

设计了 5 条高解释性的 LF，逻辑同步于 `starter/lf_template.py`：

| LF 名称 | 业务解释 | 针对问题 |
| :--- | :--- | :--- |
| `lf_cardiac_emergency` | 心内科出现的胸痛/呼吸困难/ECG异常判定为高危 | 修正 Cardiology FN |
| `lf_general_low_risk` | 全科室中的常规随访、配药等任务判定为低危 | 修正 GenMed FP |
| `lf_abnormal_lab_v2` | 基于化验异常项数量 (>2 高危, 0 低危) 的基础规则 | 通用风险覆盖 |
| `lf_late_quarter_comorbidity` | 针对 2024 后期季度，强化对多病共存患者的风险判定 | 应对时间漂移 |
| `lf_elderly_emergency` | 75岁及以上的高龄急诊患者判定为高危 | 捕捉子群体极高风险 |

**LF Summary (训练集 5000条)**:
- **Coverage**: 94.08% | **Overlap**: 63.00% | **Conflict**: 39.06%

---

## 4. 实验结果对比 (Comparison)

### 4.1 模型选择分析
在验证集上，**Majority Vote (MV)** 虽然在覆盖到的样本上精确度高，但弃权率达 34%。最终选择 **Weighted Label Model (加权模型)** 进行测试集推理，因为它通过学习权重（Cardio权重1.0, GenMed权重0.9）化解了冲突，并提供了 **92.5%** 的样本覆盖率。

### 4.2 最终测试集表现 (results/evaluation_results.txt)
- **Accuracy**: 0.8018
- **F1 Score**: **0.7248**
- **Subgroup Accuracy**: 
    - Cardiology: 1.0000 (完美捕捉风险)
    - GeneralMedicine: 0.9111 (有效过滤噪音)
    - Emergency: 0.3333 (小样本子群体，仍有改进空间)

---

## 5. 项目结构与交付清单


- `scripts/diagnose/`: 数据缺失、偏差、噪音画像脚本。
- `scripts/experiments/`: LF 迭代、模型对比及最终测试脚本。
- `results/`: 包含 `predictions.csv` (240条预测) 和 `evaluation_results.txt` (指标日志)。
- `互评作业1/starter/lf_template.py`: 最终优化的标签函数代码。
