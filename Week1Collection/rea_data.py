import os
import json
import matplotlib.pyplot as plt
import numpy as np


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def write_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


REASONING_DIR = "500reasoning_v3"

# 当前文件所在的文件夹
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# reasoning测试结果文件
TESTMODEL_LIST = [
    # 闭源
    "gpt-4o",
    "gemini-1.5-pro-001",
    "gemini-1.5-flash-001",
    "claude-3-5-sonnet-20240620",
    "qwen-vl-max-0809",
    "qwen-vl-plus-0809",
    # "glm-4v",
    # 开源
    "yi-vision",
    "internlm-xcomposer2d5-7b",
    # "internvl",
    "VILA1.5-40b",
]
DECAY_FACTOR = 0.9
ALPHA = 0.9

# 汇总数据
"""
NAME_LIST = ["hzm", "fxt", "jhy"]
for TESTMODEL in TESTMODEL_LIST:
    print(f"TESTMODEL: {TESTMODEL}")
    TOTAL_SCORE_DATA_DICT = {}
    len_total = 0
    error = False
    for NAME in NAME_LIST:
        REASONING_DIR = "./reasoning_v3"
        SCORE_FILE_PATH = os.path.join(
            CURRENT_DIR,
            NAME,
            REASONING_DIR,
            TESTMODEL + f"_reason_score_{DECAY_FACTOR}_{ALPHA}.json",
        )
        SCORE_DATA = read_json(SCORE_FILE_PATH)
        print(f"\t{NAME}: {len(SCORE_DATA)}")
        len_total += len(SCORE_DATA)
        TOTAL_SCORE_DATA_DICT.update(SCORE_DATA)
        if len(TOTAL_SCORE_DATA_DICT) != len_total:
            print(f"\t{NAME} COUNT ERROR!!!!!!!!")
            error = True
            len_total = len(TOTAL_SCORE_DATA_DICT)
    if error:
        print("ERROR!!!!!!!!")
        continue
    # 写入
    write_json(
        TOTAL_SCORE_DATA_DICT,
        os.path.join(
            CURRENT_DIR,
            REASONING_DIR,
            TESTMODEL + f"_reason_score_{DECAY_FACTOR}_{ALPHA}.json",
        ),
    )

print("DONE")
"""

# 统计数据
# 统计维度：
# 1. score_reason 平均分(mean)、取值分布
# 2. score_4o 得分率(accuracy)、取值分布
# 3. 答题hop数量（"hop_quality"里的key数量）分布
# 4. score_reason和hop数量的相关性分析（相关系数）
# 5. hop数量和参考答案hop数量的相关性分析（相关系数）、差异值分布
# 6. hop_quality细粒度分析（列表里三个数值分别代表：reasonable、precise、knowledgeable）
# - reasonable合理性：平均分、取值分布
# - precise精准性：平均分、取值分布
# - knowledgeable知识性：1和0的占比
# 7. score_reason和score_4o的相关性分析（相关系数）

# 每个维度的各模型的图都画在同一个大图里
# 11个模型，第一行闭源，第二行开源

TESTMODEL_TITLE_LIST = [
    # 调整顺序
    "GPT-4o",
    "Gemini-1.5-\nPro-001",
    "Gemini-1.5-\nFlash-001",
    "Claude-3-5-\nSonnet",
    "Qwen-VL-\nMax-0809",
    "Qwen-VL-\nPlus-0809",
    "Yi-VL-34B",
    "InternLM-\nXComposer2-VL",
    "VILA1.5",
]

CALCULATED_DATA_DICT = {}
if not os.path.exists(
    os.path.join(CURRENT_DIR, REASONING_DIR, "reasoning_data_calculated.json")
):
    write_json(
        CALCULATED_DATA_DICT,
        os.path.join(CURRENT_DIR, REASONING_DIR, "reasoning_data_calculated.json"),
    )
# 读取已经算好的数据
CALCULATED_DATA_DICT = read_json(
    os.path.join(CURRENT_DIR, REASONING_DIR, "reasoning_data_calculated.json")
)

# # 维度1：score_reason 平均分(mean)、取值分布
# plt.suptitle("Reasoning Score Distribution", fontsize=12)
for i, TESTMODEL in enumerate(TESTMODEL_LIST):
    SCORE_FILE_PATH = os.path.join(
        CURRENT_DIR,
        REASONING_DIR,
        TESTMODEL + f"_reason_score_{DECAY_FACTOR}_{ALPHA}.json",
    )
    SCORE_DATA = read_json(SCORE_FILE_PATH)
    print(f"TESTMODEL: {TESTMODEL}")
    print(f"\tTOTAL: {len(SCORE_DATA)}")
    # 1. score_reason 平均分(mean)、取值分布
    score_reason_list = []
    for key, value in SCORE_DATA.items():
        score_reason_list.append(value["reason_judge"]["score_reason"])
    print(f"\tscore_reason_mean: {sum(score_reason_list) / 500}")
    # 如果个数不足500，用0填充
    if len(score_reason_list) < 500:
        score_reason_list.extend([0] * (500 - len(score_reason_list)))
    CALCULATED_DATA_DICT[TESTMODEL] = {
        "score_reason_mean": sum(score_reason_list) / 500,
    }
    print(f"\tscore_reason_distribution:")
#     # 画出频率图
#     plt.subplot(2, 7, i + 1)
#     plt.hist(score_reason_list, bins=10, edgecolor="black", color="lightblue")
#     plt.title(TESTMODEL, fontsize=8)
#     plt.xlabel("score", fontsize=8)
#     plt.ylabel("frequency", fontsize=8)
#     # 设置x轴刻度
#     plt.xticks([0.5 * x for x in range(0, 10, 1)], fontsize=6)
#     plt.tight_layout()

# # 设置标题，位置移上
# # plt.show()
# # 保存图片
# plt.savefig(
#     os.path.join(
#         CURRENT_DIR,
#         REASONING_DIR,
#         "reasoning_score_distribution.png",
#     ),
#     # 周围空白去除
#     bbox_inches="tight",
# )


# # 维度2：score_4o 得分率(accuracy)、取值分布
# plt.suptitle("Accuracy Distribution", fontsize=12)
for i, TESTMODEL in enumerate(TESTMODEL_LIST):
    SCORE_FILE_PATH = os.path.join(
        CURRENT_DIR,
        REASONING_DIR,
        TESTMODEL + f"_reason_score_{DECAY_FACTOR}_{ALPHA}.json",
    )
    SCORE_DATA = read_json(SCORE_FILE_PATH)
    print(f"TESTMODEL: {TESTMODEL}")
    print(f"\tTOTAL: {len(SCORE_DATA)}")
    # 2. score_4o 得分率(accuracy)、取值分布
    score_4o_list = []
    for key, value in SCORE_DATA.items():
        if isinstance(value.get("ordinary_judge", {}), dict):
            score_4o = value.get("ordinary_judge", {}).get("score_4o", 0)
        else:
            score_4o = 0
        if not isinstance(score_4o, float) or not isinstance(score_4o, int):
            try:
                score_4o = float(score_4o)
            except ValueError:
                score_4o = 0
        score_4o_list.append(score_4o)
    print(f"\tscore_4o_mean: {sum(score_4o_list) / 500}")
    # 如果个数不足500，用0填充
    if len(score_4o_list) < 500:
        score_4o_list.extend([0] * (500 - len(score_4o_list)))
    CALCULATED_DATA_DICT[TESTMODEL]["score_4o_accuracy"] = sum(score_4o_list) / (
        500 * 4
    )
    print(f"\tscore_4o_distribution:")
#     # 画出频率图
#     plt.subplot(2, 7, i + 1)
#     plt.hist(score_4o_list, bins=5, edgecolor="black", color="lightblue")
#     plt.title(TESTMODEL, fontsize=8)
#     plt.xlabel("score", fontsize=8)
#     plt.ylabel("frequency", fontsize=8)
#     # 设置x轴刻度
#     plt.xticks([x for x in range(0, 5, 1)], fontsize=6)
#     plt.tight_layout()

# # 设置标题，位置移上
# # plt.show()
# # 保存图片
# plt.savefig(
#     os.path.join(
#         CURRENT_DIR,
#         REA
#         "accuracy_distribution.png",
#     ),
#     # 周围空白去除
#     bbox_inches="tight",
# )


# # 维度3：hop数量（"hop_quality"里的key数量）分布，平均值
# plt.suptitle("Hop Number Distribution", fontsize=12)
for i, TESTMODEL in enumerate(TESTMODEL_LIST):
    SCORE_FILE_PATH = os.path.join(
        CURRENT_DIR,
        REASONING_DIR,
        TESTMODEL + f"_reason_score_{DECAY_FACTOR}_{ALPHA}.json",
    )
    SCORE_DATA = read_json(SCORE_FILE_PATH)
    print(f"TESTMODEL: {TESTMODEL}")
    print(f"\tTOTAL: {len(SCORE_DATA)}")
    # 3. hop数量（"hop_quality"里的key数量）分布
    hop_quality_list = []
    for key, value in SCORE_DATA.items():
        value_ = value.get("reason_judge", {}).get("hop_quality", {})
        if not isinstance(value_, dict):
            value_ = {}
        # key的数量
        hop_quality_list.append(len(value_))
    print(f"\thop_quality_distribution:")
    print(f"\t\tmean: {sum(hop_quality_list) / 500}")
    # 如果个数不足500，用0填充
    if len(hop_quality_list) < 500:
        hop_quality_list.extend([0] * (500 - len(hop_quality_list)))
    CALCULATED_DATA_DICT[TESTMODEL]["hop_quality_mean"] = sum(hop_quality_list) / 500
#     # 画出频率图
#     plt.subplot(2, 7, i + 1)
#     plt.hist(hop_quality_list, bins=10, edgecolor="black", color="lightblue")
#     plt.title(TESTMODEL, fontsize=8)
#     plt.xlabel("number", fontsize=8)
#     plt.ylabel("frequency", fontsize=8)
#     # 设置x轴刻度
#     plt.xticks([x for x in range(0, 10, 1)], fontsize=6)
#     plt.tight_layout()

# # plt.show()
# # 保存图片
# plt.savefig(
#     os.path.join(
#         CURRENT_DIR,
#         REA
#         "hop_number_distribution.png",
#     ),
#     # 周围空白去除
#     bbox_inches="tight",
# )

# 维度4：score_reason和hop数量的相关性分析（相关系数）
# 4. score_reason和hop数量的相关性分析（相关系数）
# 4.1 计算相关系数
# 4.2 画出相关性图
# 4.3 保存图片
for i, TESTMODEL in enumerate(TESTMODEL_LIST):
    SCORE_FILE_PATH = os.path.join(
        CURRENT_DIR,
        REASONING_DIR,
        TESTMODEL + f"_reason_score_{DECAY_FACTOR}_{ALPHA}.json",
    )
    SCORE_DATA = read_json(SCORE_FILE_PATH)
    # 4.1 计算相关系数
    score_reason_list = []
    hop_quality_list = []
    for key, value in SCORE_DATA.items():
        score_reason = value.get("reason_judge", {}).get("score_reason", 0)
        hop_quality = len(value.get("reason_judge", {}).get("hop_quality", {}))
        score_reason_list.append(score_reason)
        hop_quality_list.append(hop_quality)
    # 相关系数
    correlation_coefficient = np.corrcoef(score_reason_list, hop_quality_list)[0, 1]
    CALCULATED_DATA_DICT[TESTMODEL][
        "score_reason_hop_correlation"
    ] = correlation_coefficient
    print(f"TESTMODEL: {TESTMODEL}")
    print(f"\tscore_reason_hop_correlation: {correlation_coefficient}")
#     # 4.2 画出相关性图
#     plt.subplot(2, 7, i + 1)
#     plt.scatter(score_reason_list, hop_quality_list)
#     plt.title(TESTMODEL, fontsize=8)
#     plt.xlabel("score_reason", fontsize=8)
#     plt.ylabel("hop_quality", fontsize=8)
#     plt.tight_layout()

# # 4.3 保存图片
# # plt.show()
# plt.savefig(
#     os.path.join(
#         CURRENT_DIR,
#         REA
#         "reasoning_score_hop_correlation.png",
#     ),
# )

# 维度5：hop数量和参考答案hop数量的相关性分析（相关系数）、差异值分布
# 5.1 获取参考答案hop数量和模型hop数量进行匹配
# 5.2 计算相关系数
# 5.3 画出相关性图
# 5.4 保存图片
# 5.5 计算差异值分布
# 5.6 画出差异值分布
# 5.7 保存图片
# 5.8 计算差异值的平均值
NAME_LIST = ["hzm", "fxt", "jhy"]
# 获取参考答案hop数量
DATA_DICT = {}
for NAME in NAME_LIST:
    if NAME == "hzm" or NAME == "fxt":
        DATA_FILE_PATH = os.path.join(
            CURRENT_DIR,
            NAME,
            "labels_test.json",
        )
    else:
        DATA_FILE_PATH = os.path.join(
            CURRENT_DIR,
            NAME,
            "random_labels.json",
        )
    data = read_json(DATA_FILE_PATH)
    for item in data:
        foldername = item["foldername"]
        DATA_DICT[foldername] = {"ref_hop_count": item["hop_count"]}
print(len(DATA_DICT))

# 获取模型hop数量
for i, TESTMODEL in enumerate(TESTMODEL_LIST):
    print(f"TESTMODEL: {TESTMODEL}")
    SCORE_FILE_PATH = os.path.join(
        CURRENT_DIR,
        REASONING_DIR,
        TESTMODEL + f"_reason_score_{DECAY_FACTOR}_{ALPHA}.json",
    )
    SCORE_DATA = read_json(SCORE_FILE_PATH)
    for key, value in SCORE_DATA.items():
        if key in DATA_DICT:
            DATA_DICT[key][f"model_hop_count_{TESTMODEL}"] = len(
                value.get("reason_judge", {}).get("hop_quality", {})
            )
        else:
            print(f"\tError: key: {key} not in DATA_DICT")
    print(f"\tTOTAL: {len(SCORE_DATA)}")
    print(f"\tDATA_DICT: {len(DATA_DICT)}")
    # 保存DATA_DICT
    write_json(
        DATA_DICT,
        os.path.join(CURRENT_DIR, REASONING_DIR, "hop_count_data.json"),
    )
    # 计算相关系数
    ref_hop_count_list = []
    model_hop_count_list = []
    for key, value in DATA_DICT.items():
        ref_hop_count_list.append(value.get("ref_hop_count", 0))
        model_hop_count_list.append(value.get(f"model_hop_count_{TESTMODEL}", 0))
    correlation_coefficient = np.corrcoef(ref_hop_count_list, model_hop_count_list)[
        0, 1
    ]
    CALCULATED_DATA_DICT[TESTMODEL]["hop_count_correlation"] = correlation_coefficient
    print(f"\tcorrelation_coefficient: {correlation_coefficient}")
#     # 画出相关性图
#     plt.subplot(2, 7, i + 1)
#     plt.scatter(ref_hop_count_list, model_hop_count_list)
#     plt.title(TESTMODEL, fontsize=8)
#     plt.xlabel("ref_hop_count", fontsize=8)
#     plt.ylabel("model_hop_count", fontsize=8)
#     plt.tight_layout()
# # 保存图片
# plt.savefig(
#     os.path.join(
#         CURRENT_DIR,
#         REA
#         "hop_count_correlation.png",
#     ),
# )


# 维度6：hop_quality细粒度分析（列表里三个数值分别代表：reasonable、precise、knowledgeable）
# 6.1 计算每个维度的平均分
# 6.2 画出每个维度的取值分布
# 6.3 保存图片
for i, TESTMODEL in enumerate(TESTMODEL_LIST):
    print(f"TESTMODEL: {TESTMODEL}")
    SCORE_FILE_PATH = os.path.join(
        CURRENT_DIR,
        REASONING_DIR,
        TESTMODEL + f"_reason_score_{DECAY_FACTOR}_{ALPHA}.json",
    )
    SCORE_DATA = read_json(SCORE_FILE_PATH)
    reasonable_list = []
    precise_list = []
    knowledgeable_list = []
    for key, value in SCORE_DATA.items():
        hop_quality = value.get("reason_judge", {}).get("hop_quality", {})
        if not isinstance(hop_quality, dict):
            hop_quality = {}
        for hop_quality_key, hop_quality_value in hop_quality.items():
            if isinstance(hop_quality_value, list) and len(hop_quality_value) == 3:
                reasonable = hop_quality_value[0]
                precise = hop_quality_value[1]
                knowledgeable = (
                    hop_quality_value[2]
                    if hop_quality_value[2] in [0, 1]
                    else (
                        0
                        if hop_quality_value[2] < 0.5
                        else 1 if hop_quality_value[2] > 0.5 else 0
                    )
                )
                reasonable_list.append(reasonable)
                precise_list.append(precise)
                knowledgeable_list.append(knowledgeable)
            else:
                print(f"\tError: {hop_quality_key} is not a list of 3 elements")
    print(f"\treasonable_mean: {sum(reasonable_list) / len(reasonable_list)}")
    print(f"\tprecise_mean: {sum(precise_list) / len(precise_list)}")
    print(f"\tknowledgeable_mean: {sum(knowledgeable_list) / len(knowledgeable_list)}")
    CALCULATED_DATA_DICT[TESTMODEL]["knowledgeable_mean"] = sum(
        knowledgeable_list
    ) / len(knowledgeable_list)
    CALCULATED_DATA_DICT[TESTMODEL]["precise_mean"] = sum(precise_list) / len(
        precise_list
    )
    CALCULATED_DATA_DICT[TESTMODEL]["reasonable_mean"] = sum(reasonable_list) / len(
        reasonable_list
    )

# # 画出取值分布
#     plt.subplot(2, 7, i + 1)
#     plt.hist(knowledgeable_list, bins=2, edgecolor="black", color="lightblue")
#     plt.title(TESTMODEL, fontsize=8)
#     plt.xlabel("knowledgeable", fontsize=8)
#     plt.ylabel("frequency", fontsize=8)
#     plt.tight_layout()

# # 保存图片
# plt.savefig(
#     os.path.join(
#         CURRENT_DIR,
#         REASONING_DIR,
#         "knowledgeable_distribution.png",
#     ),
# )


# 维度7：score_reason和score_4o的相关性分析（相关系数）
# 7.1 计算相关系数
# 7.2 画出相关性图
# 7.3 保存图片
# 标题
# plt.suptitle("Reasoning Score and 4o Score Correlation", fontsize=12)
for i, TESTMODEL in enumerate(TESTMODEL_LIST):
    print(f"TESTMODEL: {TESTMODEL}")
    SCORE_FILE_PATH = os.path.join(
        CURRENT_DIR,
        REASONING_DIR,
        TESTMODEL + f"_reason_score_{DECAY_FACTOR}_{ALPHA}.json",
    )
    SCORE_DATA = read_json(SCORE_FILE_PATH)
    score_reason_list = []
    score_4o_list = []
    for key, value in SCORE_DATA.items():
        if isinstance(value.get("ordinary_judge", {}), dict):
            score_4o = value.get("ordinary_judge", {}).get("score_4o", 0)
        else:
            score_4o = 0
        if isinstance(value.get("reason_judge", {}), dict):
            score_reason = value.get("reason_judge", {}).get("score_reason", 0)
        else:
            score_reason = 0
        if not isinstance(score_reason, float) or not isinstance(score_reason, int):
            try:
                score_reason = float(score_reason)
            except ValueError:
                score_reason = 0
        if not isinstance(score_4o, float) or not isinstance(score_4o, int):
            try:
                score_4o = float(score_4o)
            except ValueError:
                score_4o = 0
        score_reason_list.append(score_reason)
        score_4o_list.append(score_4o)
    # 相关系数
    # 如果个数不足500，用0填充
    if len(score_reason_list) < 500:
        score_reason_list.extend([0] * (500 - len(score_reason_list)))
    if len(score_4o_list) < 500:
        score_4o_list.extend([0] * (500 - len(score_4o_list)))
    correlation_coefficient = np.corrcoef(score_reason_list, score_4o_list)[0, 1]
    CALCULATED_DATA_DICT[TESTMODEL][
        "score_reason_score_4o_correlation"
    ] = correlation_coefficient
    print(f"\tscore_reason_score_4o_correlation: {correlation_coefficient}")
#     # 画出相关性图
#     plt.subplot(2, 7, i + 1)
#     plt.scatter(score_reason_list, score_4o_list)
#     plt.title(TESTMODEL, fontsize=8)
#     plt.xlabel("score_reason", fontsize=8)
#     plt.ylabel("score_4o", fontsize=8)
#     plt.tight_layout()

# # 保存图片
# plt.savefig(
#     os.path.join(
#         CURRENT_DIR,
#         REASONING_DIR,
#         "score_reason_score_4o_correlation.png",
#     ),
# )
# 保存数据（json）
write_json(
    CALCULATED_DATA_DICT,
    os.path.join(
        CURRENT_DIR,
        REASONING_DIR,
        "reasoning_data_calculated.json",
    ),
)
