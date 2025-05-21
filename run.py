import os
import warnings
from method import *

warnings.filterwarnings("ignore")

GENERATOR_MODELS = [
    # "llama2-7B-chat",
    # "llama2-13B-chat",
    "llama3-8B-instruct",
    # "gpt-4o-mini-2024-07-18",
]

DATASET_NAMES = {
    "dp_dataset": {
        "hotpotqa": [
            # "t1_2hop_bridge",
            # "t2_2hop_comparison",
        ],
        "2wikimultihopqa": [
            # "t1_2hop_bridge",
            # "t2_2hop_comparison",
            # "t3_2hop_inference",
            # "t9_4hop_comparison",
            # "t10_4hop_bridge_comparison",
        ],
        "musique": [
            # "t1_2hop_bridge",
            # "t4_3hop_bridge",
            # "t5_3hop_bridge",
            # "t6_4hop_bridge",
            # "t7_4hop_bridge",
            # "t8_4hop_bridge",
        ]
    },
    "method_dataset": {
        "hotpotqa": [
            "2hop_bridge",
            "2hop_comparison",
        ],
        "2wikimultihopqa": [
            "2hop_bridge",
            "2hop_comparison",
            "2hop_inference",
            "4hop_comparison",
            "4hop_bridge_comparison",
        ],
        "musique": [
            "2hop_bridge",
            "3hop_bridge",
            "4hop_bridge",
        ]
    }
}

FUNC_DICT = {
    "per_dp": per_dp,
    "per_qa_chat": per_qa_chat,
    "per_qa_rag": per_qa_rag,
    "zeroshot": zeroshot,
    "naive_rag": naiverag,
    "selfask": selfask,
    "ircot": ircot,
}


if __name__ == '__main__':
    method_name = "per_qa_rag"
    test_sample_num = 1
    data_dir = "datasets/YOUR_DATA_TO_PREPROCESS" if method_name == "per_dp" else "datasets/YOUR_DATA"
    data_name = "dp_dataset" if method_name == "per_dp" else "method_dataset"
    save_dir = "output/example"
    os.makedirs(save_dir, exist_ok=True)

    for generator_model in GENERATOR_MODELS:
        for dataset_name, splits in DATASET_NAMES[data_name].items():
            for split in splits:

                CONFIG_DICT = {
                    # Environment Settings
                    "data_dir": data_dir,
                    "dataset_name": dataset_name,
                    "split": split,
                    "test_sample_num": test_sample_num,
                    "seed": 2048,
                    "random_sample": False,
                    "method_name": method_name,
                    "save_dir": save_dir,
                    "save_note": f"{dataset_name}_{split}_{method_name}_{generator_model}",

                    # Generator Settings
                    "framework": "hf" if "llama" in generator_model else "openai",
                    "generator_model": generator_model,
                }

                func = FUNC_DICT[CONFIG_DICT["method_name"]]
                func(CONFIG_DICT)
