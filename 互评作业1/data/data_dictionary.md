# 课程版医疗数据治理数据字典

## 数据集概览

- 数据集名称：课程版医疗数据治理数据集
- 数据来源：公开 Synthea 合成患者数据（100-patient 子集）
- 来源地址：`https://raw.githubusercontent.com/lhs-open/synthetic-data/main/record/synthea-dataset-100.zip`
- 随机种子：`42`
- 训练集规模：`5000`
- 验证集规模：`120`
- 测试集规模：`240`

## 标签说明

- `risk_label_noisy`：训练过程可见的噪音标签
- `risk_label_clean`：仅用于验证集和测试集的干净标签
- `split`：`train_unlabeled` / `validation_small` / `test_labeled`

## 课程化处理说明

本数据包由公开 Synthea 子集加工而来，教师侧会统一注入：

- 缺失机制差异（MCAR / MAR / MNAR 风格）
- 标签噪音（科室 / 时间 / 子群体相关）
- 时间漂移（后期季度信号变化）
- 可用于编写 LF 的明显线索

## 源数据概览

- 原始患者数：`140`
- 原始就诊数：`12361`
- 原始条件数：`7708`
- 原始药物数：`14016`
- 原始观测数：`100402`

## 字段说明

| 字段名 | 类型 | 示例 | 字段含义 | 是否可能缺失 | 备注 |
|---|---|---|---|---|---|
| `patient_id` | string | `P000123` | 患者唯一标识 | 否 | 已匿名化 |
| `visit_id` | string | `V000123_01` | 就诊记录唯一标识 | 否 | 已匿名化 |
| `age_group` | category | `60-74` | 年龄分组 | 否 | 用于分组分析 |
| `gender` | category | `F` | 性别 | 否 | 用于分组分析 |
| `department` | category | `Cardiology` | 科室 | 否 | 可作为分层条件 |
| `admission_type` | category | `Emergency` | 就诊类型 | 否 | 可用于 LF |
| `visit_time_bucket` | category | `Night` | 时间段 | 否 | 可用于 LF |
| `prior_visit_count` | integer | `3` | 既往就诊次数 | 否 | 可用于阈值 LF |
| `lab_abnormal_count` | integer | `2` | 异常检验项数量 | 是 | 可用于阈值 LF |
| `med_count` | integer | `4` | 药物数量 | 是 | 可能含 MAR 缺失 |
| `comorbidity_count` | integer | `2` | 共病数量 | 否 | 可用于结构化风险判定 |
| `length_of_stay_proxy` | float | `2.5` | 停留时长代理变量 | 是 | 可用于漂移与缺失分析 |
| `year_quarter` | category | `2024Q3` | 时间季度 | 否 | 用于时间漂移分析 |
| `hospital_unit` | category | `Unit_B` | 医疗单元 | 否 | 用于分组分析 |
| `chief_complaint` | string | `chest pain and shortness of breath` | 主诉文本 | 否 | 文本 LF 主要字段 |
| `triage_note` | string | `abnormal ECG, repeated visit this month` | 分诊简述 | 是 | 文本 LF 辅助字段 |
| `risk_label_noisy` | integer | `1` | 历史流程产生的噪音标签 | 可选 | 建议仅训练集使用 |
| `risk_label_clean` | integer | `1` | 干净标签 | 否 | 仅验证集/测试集公开 |
| `split` | category | `train_unlabeled` | 数据集划分 | 否 | `train_unlabeled`/`validation_small`/`test_labeled` |
