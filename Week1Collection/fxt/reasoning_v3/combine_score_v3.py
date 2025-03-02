import json
import os
import sys

# 当前路径
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# 得分文件路径
SCORE_V3_DIR = "C:/Hzimeng/College/SYSU/ScienceResearch/dataset_test/demo-reasoning/test_and _judge/RIA/fxt"
TESTMODEL_LIST = [
    "gpt-4o",
    "gemini-1.5-pro-001",
    "gemini-1.5-flash-001",
    "claude-3-5-sonnet-20240620",
    "yi-vision",
    # "glm-4v",
    "internlm-xcomposer2d5-7b",
    # "internvl",
    "qwen-vl-max-0809",
    "qwen-vl-plus-0809",
    "VILA1.5-40b",
]
for TESTMODEL in TESTMODEL_LIST:
    COMBINE_PATH = os.path.join(CURRENT_PATH, f"{TESTMODEL}_reason_combine.json")
    with open(COMBINE_PATH, "r", encoding="utf-8") as f:
        combine_data_before = json.load(f)

    SCORE_V3_PATH = os.path.join(
        SCORE_V3_DIR, f"{TESTMODEL}_test_and_judge_new_ds.json"
    )
    with open(SCORE_V3_PATH, "r", encoding="utf-8") as f:
        score_v3_data = json.load(f)

    combine_data_after = combine_data_before.copy()
    for foldername, value in combine_data_before.items():
        if foldername in score_v3_data:
            combine_data_after[foldername]["MLLM_answer"] = (
                score_v3_data[foldername]["MLLM_answer"]
                if "MLLM_answer" in score_v3_data[foldername]
                else ""
            )
            combine_data_after[foldername]["ordinary_judge"] = (
                score_v3_data[foldername]["judge_answer"]
                if "judge_answer" in score_v3_data[foldername]
                else {
                    "score_4o": 0,
                    "score_reason": "Error",
                }
            )
        else:
            combine_data_after[foldername]["MLLM_answer"] = ""
            combine_data_after[foldername]["ordinary_judge"] = {
                "score_4o": 0,
                "score_reason": "Error",
            }
        # combine_data_after[foldername]删除judge_answer
        if "judge_answer" in combine_data_after[foldername]:
            combine_data_after[foldername].pop("judge_answer")

    with open(COMBINE_PATH, "w", encoding="utf-8") as f:
        json.dump(combine_data_after, f, ensure_ascii=False, indent=4)
    print(f"{TESTMODEL} done")
