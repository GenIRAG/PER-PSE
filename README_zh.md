# Beyond the Answer: Advancing Multi-Hop QA with Fine-Grained Graph Reasoning and Evaluation

\[ [English](README.md) | 中文 \]

<div align="center"> 

[![Paper](https://img.shields.io/badge/Paper-ACL-red)]() [![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/GenIRAG/PER-PSE/blob/main/LICENSE) [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3112/) 
</div>

## ✨ 介绍
<p align="center">

<img src="figures/framework.jpg">
</p>

大型语言模型 (LLM) 的最新进展显著提升了多跳问答 (MHQA) 系统的性能。尽管 MHQA 系统取得了成功，但对其评估的研究尚不深入。现有的评估主要侧重于比较推理方法的最终答案与给定的 ground-truth。我们认为，推理过程也应该进行评估，因为错误的推理过程也可能产生正确的最终答案。受此启发，我们提出了一种“<u>**P**</u>lanner-<u>**E**</u>executor-<u>**R**</u>easoner”（PER）架构，它构成了“规划划锚定数据预处理” (Plan-anchored Data Preprocessing, PER-DP) 和“规划引导多跳问答” (Plan-guided Multi-Hop QA, PER-QA) 的核心。前者提供中间推理步骤和最终答案的 ground-truth，后者提供推理方法的 ground-truth。此外，我们设计了一种名为<u>**P**</u>lan-aligned <u>**S**</u>tepwise <u>**E**</u>valuation (PSE) 的细粒度评估指标，该指标从规划和求解两个角度评估中间推理步骤。针对十类问题的大量实验证明了该模型具有竞争性的推理性能，提升了 MHQA 系统的可解释性，并揭示了基于 RAG 的 MHQA 系统中诸如“侥幸的推理继续”和“潜在的推理暂停”等问题。此外，我们还展示了该方法在数据污染场景中的潜力。

## 📦 环境

``` pip
pip install -r requirement.txt
```

## 🗄️ 数据

我们公开了经过PRE-DP处理的多跳问答数据集，包括HotpotQA、2WikiMultihopQA和MuSiQue，共计8394条。数据可以从[Huggingface Datasets](https://huggingface.co/datasets/GenIRAG/PER-PSE)下载。

**数据集格式：**
```jsonl
{
    "id": 问题标识符,
    "question": 问题,
    "golden_answers": [
        黄金答案1, 
        ...
    ],

    "metadata":{
        "_id": 原数据集中问题标识符,
        "type": 问题类型，"bridge"或"compositional",
        "hop": 问题跳数，例如"2hop",
        "plan": {
            // 分解后的问题规划
            "Q1": [
                子问题1,
                占位符1，例如"<A1>"
            ],
            ...
        },
        "graph": [
            // 分解后问题的实例化图
            {
                "Q1": {
                    "template": 分解后问题模板（含占位符）,
                    "previous": [依赖问题1, ...],
                    "query": 实例化后问题（不含占位符）,
                    "supports": [
                        // 黄金文档
                        {
                            "title": 文档标题,
                            "contents": [
                                文档内容,
                                ...
                            ]
                        }
                    ],
                    "tag": 占位符,
                    "answer": 子问题答案
                },
                ...
            }
        ]
    }
}
```
数据集统一使用.jsonl格式存储。`metadata`字段是经由PER-DP处理后提供的精细中间步骤。

**自定义数据集：**

可按照所提供jsonl中的格式整理自定义数据集，并配置相关参数（见下）。之后PER-PSE将按照这一格式读取、运行并产生结果。

## 🚀 运行

本项目fork自开源项目[FlashRAG](https://github.com/RUC-NLPIR/FlashRAG)并修改。运行本项目的步骤如下：

1. 在`flashrag/config/basic_config.yaml`中添加相关参数（模型路径、API密钥等）

2. 参考FlashRAG原仓库下载 BM25 索引并将其放入`indexes`中。将数据放入`datasets`下

3. 在`run.py`中配置运行参数：
- 在参数`data_dir`中设置数据存储路径
- 在参数`GENERATOR_MODELS`中设置要使用的模型
- 在参数`DATASET_NAMES`中设置要运行的数据集
- 在参数`FUNC_DICT`中选择要运行的方法
- 在main方法下设置其他参数（如日志存储路径）

4. 运行`run.py`

## 🔖 许可证

本项目根据[MIT许可证](LICENSE)授权。

## 🔭 引用
欢迎引用本文：
```bibtex
Coming Soon
```
