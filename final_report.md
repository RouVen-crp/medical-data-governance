# 医疗数据治理与弱标注作业报告

## 1. 数据问题诊断 (Evidence-based Diagnosis)

通过执行 `advanced_diagnose.py`，识别出以下核心数据治理问题：

### 1.1 缺失机制分析
- **lab_abnormal_count**: 缺失率较低 (~3%)，在急诊科 (Emergency) 缺失最低 (1.25%)，符合急诊指标必填的业务逻辑。
- **length_of_stay_proxy**: 在心内科 (Cardiology) 缺失率最高 (21%)，呈现明显的 **MAR (Missing at Random)** 特征。在编写 LF 时，对该字段的缺失处理直接影响了覆盖率。

### 1.2 标签噪音画像
对比 `risk_label_noisy` 与 `risk_label_clean` (不一致率 15.8%)：
- **False Positives (FP)**: 82% 的虚报集中在 **GeneralMedicine** 科室，说明历史标签对全科常规病例（如常规随访、开药）存在过度判定风险。
- **False Negatives (FN)**: 75% 的漏报集中在 **Cardiology** 科室，历史标签漏掉了部分胸痛等高危心内科指标。

### 1.3 时间漂移与子群体差异
- **时间漂移**: 真实风险率从 2024Q2 的 **25.9%** 飙升至 2024Q4 的 **58.0%**，表明后期季度的患者严重程度或判定门槛发生了系统性偏移。
- **子群体偏见**: Cardiology 和 Emergency 是极端高危组 (100% 风险)，而 GeneralMedicine 是极低危组 (7.9%)。

---

## 2. 标签函数 (LFs) 设计与实现

本实验设计了 5 条具备高解释性的 LF，分别对应上述诊断出的问题点：

| LF 名称 | 业务解释 | 针对问题 |
| :--- | :--- | :--- |
| `lf_cardiac_emergency` | 心内科出现的胸痛/呼吸困难/ECG异常判定为高危 | 修正 Cardiology FN |
| `lf_general_low_risk` | 全科科室中的常规随访、配药等任务判定为低危 | 修正 GenMed FP |
| `lf_abnormal_lab_v2` | 基于化验异常项数量 (>2 高危, 0 低危) 的基础规则 | 通用风险覆盖 |
| `lf_late_quarter_comorbidity` | 针对 2024 后期季度，强化对多病共存患者的风险判定 | 应对时间漂移 |
| `lf_elderly_emergency` | 75岁及以上的高龄急诊患者判定为高危 | 捕捉子群体极高风险 |

---

## 3. LF Summary 分析与迭代 (Iteration)

基于 5000 条训练数据的统计：
- **LF Coverage**: **94.08%** (几乎覆盖全量数据)
- **LF Overlap Rate**: **63.00%**
- **LF Conflict Rate**: **39.06%**

**迭代优化说明**：
- **初始阶段**: `lf_dept_bias` 过于激进，导致 Precision 仅为 0.52。
- **迭代动作**: 将 `lf_dept_bias` 细化为 `lf_cardiac_emergency` 和 `lf_general_low_risk`，并增加了对常规任务的弃权逻辑，将 Accuracy 从 0.53 提升至 **0.87**。

---

## 4. 实验效果与分析 (Comparison)

在验证集上对比了 **Majority Vote (多数投票)** 与 **Weighted Label Model (加权标签模型)**：

| 指标 | Majority Vote (MV) | Label Model (Weighted) |
| :--- | :--- | :--- |
| **Accuracy** | **0.8734** | 0.8018 |
| **F1 Score** | **0.8214** | 0.7250 |
| **Coverage** | 65.83% | **92.50%** |

**结论分析**：
1. **MV 优势**: 在冲突时选择弃权，因此在已覆盖样本上拥有更高的准确率 (Precision 0.88)。
2. **LM 优势**: 通过学习 LF 权重 (Cardio规则权重为 1.0, GenMed规则权重 0.90)， LM 能够解决冲突并提供高达 **92.5%** 的软标签覆盖，为下游深度学习模型提供更丰富的训练集。
3. **Worst-group Gap**: Cardiology 组准确率达 1.00，但 Emergency 组仅 0.33，说明急诊科的罕见重症仍需进一步特征工程。

---

## 5. 附录：提交文件清单
- `starter/lf_template.py`: 优化后的核心 LF 代码。
- `advanced_diagnose.py`: 循证分析脚本。
- `label_model_experiment.py`: MV vs LM 对照实验脚本。
- `analyze_v2.py`: 覆盖率与子群体分析脚本。
