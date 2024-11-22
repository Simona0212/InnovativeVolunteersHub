import json
import os
import random
import shutil


# 获取当前文件夹下的直接子文件夹
def get_immediate_subdirectories(a_dir):
    return [
        name
        for name in os.listdir(
            a_dir
        )  # 获取当前文件夹下的所有文件和文件夹; name是文件名或文件夹名
        if os.path.isdir(os.path.join(a_dir, name))
    ]  # 判断是否是文件夹


# 获取当前文件夹下的所有文件
def get_immediate_files(a_dir):
    return [
        name
        for name in os.listdir(a_dir)  # 获取当前文件夹下的所有文件和文件夹
        if os.path.isfile(os.path.join(a_dir, name))
    ]  # 判断是否是文件


# 读取json文件
def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# 写入json文件
def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # get the directory of this file
TOTAL_RIA_PATH = os.path.join(BASE_DIR, "Week1Collection")
MULTI_PATH = os.path.join(BASE_DIR, "Multi_Images")
PURE_SINGLE_PATH = os.path.join(BASE_DIR, "Pure_Single_Images")
INCONTEXT_PATH = os.path.join(BASE_DIR, "Incontext_Images")

SAMPLE_PURE_SINGLE_PATH = os.path.join(BASE_DIR, "SampleAnalysis", "pure_single")
SAMPLE_MULTI_PATH = os.path.join(BASE_DIR, "SampleAnalysis", "multi")
SAMPLE_INCONTEXT_PATH = os.path.join(BASE_DIR, "SampleAnalysis", "in-context")

# ================== Sample In-context ==================
# 读取所有in-context文件夹下的数据，随机抽取30个放入SampleAnalysis/in-context文件夹下
# incontext_name_list = get_immediate_subdirectories(INCONTEXT_PATH)
# incontext_data_list = list()
# incontext_data_dict = dict()
# perfect_cnt = 0
# all_perfect_cnt = 0
# for name in incontext_name_list:
#     data_incontext_path = os.path.join(INCONTEXT_PATH, name, "data_context.json")
#     data_incontext = read_json(data_incontext_path)
#     data_incontext_judge_test_path = os.path.join(
#         INCONTEXT_PATH, name, "test_and_judge_gpt-4o.json"
#     )
#     data_incontext_judge_test = read_json(data_incontext_judge_test_path)
#     # 合并数据和评测4o结果
#     for item in data_incontext:
#         foldername = item["foldername"]
#         if foldername not in data_incontext_judge_test:
#             print(f"Error: {foldername} not in data_incontext_judge_test")
#             print(f"name: {name}")
#         else:
#             item["test_results"] = data_incontext_judge_test[foldername]
#             all_perfect = True
#             for result in item["test_results"]:
#                 if (
#                     result["judge_answer"] is not None
#                     and result["judge_answer"]["score_4o"] == "4"
#                 ):
#                     perfect_cnt += 1
#                 else:
#                     all_perfect = False
#             if all_perfect:
#                 all_perfect_cnt += 1
#     incontext_data_list.extend(data_incontext)
#     sub_incontext_dict = dict()
#     for item in data_incontext:
#         item["name"] = name
#         sub_incontext_dict[item["foldername"]] = item
#     # 检查是否有重复的key
#     if not set(incontext_data_dict.keys()).isdisjoint(set(sub_incontext_dict.keys())):
#         # isdisjoint() 方法用于判断两个集合是否包含相同的元素，如果没有返回 True，否则返回 False。
#         print("Warning: Duplicate key in incontext_data dict")
#         print("Duplicate key is:")
#         for key in set(incontext_data_dict.keys()).intersection(
#             set(sub_incontext_dict.keys())
#         ):
#             print(key)
#             print("current name", name)
#             print("before name", incontext_data_dict[key]["name"])
#     incontext_data_dict.update(sub_incontext_dict)

# print(f"Total in-context: {len(incontext_data_list) * 4}")
# print(f"Perfect in-context: {perfect_cnt}")
# print(f"In-context group cnt: {len(incontext_data_list)}")
# print(f"All perfect in-context group cnt: {all_perfect_cnt}")
# print()
# # 舍弃all_perfect的数据或有Error的数据
# incontext_data_list = [
#     item
#     for item in incontext_data_list
#     if "test_results" in item
#     and all(
#         result["judge_answer"] is not None and result["judge_answer"]["score_4o"] != "4"
#         for result in item["test_results"]
#     )
# ]
# print(f"Non-perfect in-context  group cnt: {len(incontext_data_list)}")


# # 随机抽取30个
# random.shuffle(incontext_data_list)
# random.shuffle(incontext_data_list)
# random.shuffle(incontext_data_list)
# # random.shuffle() 方法将序列的所有元素随机排，内部使用的是Fisher–Yates shuffle算法
# sample_incontext_data = incontext_data_list[:30]
# # 先统计一下4o的分数分布，如果缺少某个分数，需要补充，如果分布不均匀，需要调整
# score_4o_cnt = dict()
# for item in sample_incontext_data:
#     for result in item["test_results"]:
#         score_4o = result["judge_answer"]["score_4o"]
#         if score_4o not in score_4o_cnt:
#             score_4o_cnt[score_4o] = 0
#         score_4o_cnt[score_4o] += 1
# print("Score 4o distribution:")
# print(score_4o_cnt)
# print()
# # 补充缺少的分数
# for score_4o in ["0", "1", "2", "3"]:
#     if score_4o not in score_4o_cnt:
#         print(f"Warning: Missing score {score_4o}")
#         is_break = False
#         for item in incontext_data_list:
#             for result in item["test_results"]:
#                 if result["judge_answer"]["score_4o"] == score_4o:
#                     print(f"Add {item['foldername']} to sample_incontext_data")
#                     sample_incontext_data.append(item)
#                     score_4o_cnt[score_4o] = 1
#                     is_break = True
#                     break
#             if is_break:
#                 break
# # 如果3分少于2分的1/3，需要调整
# # 由于一个item有4个result，所以加入时要统计其它result的分数
# while score_4o_cnt["3"] < score_4o_cnt["2"] // 3:
#     print("Warning: Adjust 3 score")
#     is_break = False
#     for item in incontext_data_list:
#         for result in item["test_results"]:
#             if result["judge_answer"]["score_4o"] == "3":
#                 print(f"Add {item['foldername']} to sample_incontext_data")
#                 sample_incontext_data.append(item)
#                 # 更新分数统计
#                 for result in item["test_results"]:
#                     score_4o = result["judge_answer"]["score_4o"]
#                     score_4o_cnt[score_4o] += 1
#                 is_break = True
#                 break
#         if is_break:
#             break
# # 再次统计一下4o的分数分布
# score_4o_cnt = dict()
# for item in sample_incontext_data:
#     for result in item["test_results"]:
#         score_4o = result["judge_answer"]["score_4o"]
#         if score_4o not in score_4o_cnt:
#             score_4o_cnt[score_4o] = 0
#         score_4o_cnt[score_4o] += 1
# print("Score 4o distribution after adjustment:")
# print(score_4o_cnt)
# print()

# for item in sample_incontext_data:
#     foldername = item["foldername"]
#     name = item["name"]
#     print(f"Copy {foldername} from {name} to SampleAnalysis/in-context")
#     # copy image
#     src_image_dir_path = os.path.join(INCONTEXT_PATH, name, "img", foldername)
#     dst_image_dir_path = os.path.join(SAMPLE_INCONTEXT_PATH, "images", foldername)
#     if not os.path.exists(dst_image_dir_path):
#         os.makedirs(dst_image_dir_path)
#     for image_name in get_immediate_files(src_image_dir_path):
#         src_image_path = os.path.join(src_image_dir_path, image_name)
#         dst_image_path = os.path.join(dst_image_dir_path, image_name)
#         shutil.copyfile(src_image_path, dst_image_path)
# # copy data_incontext.json
# sample_incontext_data_path = os.path.join(SAMPLE_INCONTEXT_PATH, "sample.json")
# write_json(sample_incontext_data_path, sample_incontext_data)

# ================== Sample Multi ==================
# multi 和 incontext的处理方式类似
# 读取所有multi文件夹下的数据，随机抽取30个放入SampleAnalysis/multi文件夹下
multi_name_list = get_immediate_subdirectories(MULTI_PATH)
multi_data_list = list()
multi_data_dict = dict()
perfect_cnt = 0
all_perfect_cnt = 0
all_multi_cnt = 0
for name in multi_name_list:
    data_multi_path = os.path.join(MULTI_PATH, name, "data_multi.json")
    data_multi = read_json(data_multi_path)
    data_multi_judge_test_path = os.path.join(
        MULTI_PATH, name, "gpt-4o_multi_test_and_judge_complete.json"
    )
    data_multi_judge_test = read_json(data_multi_judge_test_path)
    # 合并数据和评测4o结果
    for item in data_multi:
        foldername = item["foldername"]
        if foldername not in data_multi_judge_test:
            print(f"Error: {foldername} not in data_multi_judge_test")
            print(f"name: {name}")
        else:
            item["test_results"] = data_multi_judge_test[foldername]
            all_perfect = True
            if not isinstance(item["test_results"], list):
                print(f"Error: {foldername} test_results is not list")
                print(f"name: {name}")
            for result in item["test_results"]:
                all_multi_cnt += 1
                if (
                    result["judge_answer"] is not None
                    and result["judge_answer"] != "Error"
                    and result["judge_answer"]["score_4o"] == "4"
                ):
                    perfect_cnt += 1
                else:
                    all_perfect = False
            if all_perfect:
                all_perfect_cnt += 1

    multi_data_list.extend(data_multi)
    sub_multi_dict = dict()
    for item in data_multi:
        item["name"] = name
        sub_multi_dict[item["foldername"]] = item
    # 检查是否有重复的key
    if not set(multi_data_dict.keys()).isdisjoint(set(sub_multi_dict.keys())):
        # isdisjoint() 方法用于判断两个集合是否包含相同的元素，如果没有返回 True，否则返回 False。
        print("Warning: Duplicate key in multi_data dict")
        print("Duplicate key is:")
        for key in set(multi_data_dict.keys()).intersection(set(sub_multi_dict.keys())):
            print(key)
            print("current name", name)
            print("before name", multi_data_dict[key]["name"])
    multi_data_dict.update(sub_multi_dict)

print(f"Total multi images: {all_multi_cnt}")
print(f"Perfect multi images: {perfect_cnt}")
print(f"Multi group cnt: {len(multi_data_list)}")
print(f"All perfect multi group cnt: {all_perfect_cnt}")
print()
# 舍弃perfect的数据
multi_data_list = [
    item
    for item in multi_data_list
    if "test_results" in item
    and all(
        result["judge_answer"] is not None and result["judge_answer"]["score_4o"] != "4"
        for result in item["test_results"]
    )
]
print(f"Non-perfect multi images: {len(multi_data_list)}")

# 随机抽取30个
random.shuffle(multi_data_list)
random.shuffle(multi_data_list)
random.shuffle(multi_data_list)
# random.shuffle() 方法将序列的所有元素随机排，内部使用的是Fisher–Yates shuffle算法
sample_multi_data = multi_data_list[:30]
# 先统计一下4o的分数分布，如果缺少某个分数，需要补充，如果分布不均匀，需要调整
score_4o_cnt = dict()
for item in sample_multi_data:
    score_4o = item["judge_answer"]["score_4o"]
    if score_4o not in score_4o_cnt:
        score_4o_cnt[score_4o] = 0
    score_4o_cnt[score_4o] += 1
print("Score 4o distribution:")
print(score_4o_cnt)
print()
# 补充缺少的分数
for score_4o in ["0", "1", "2", "3"]:
    if score_4o not in score_4o_cnt:
        print(f"Warning: Missing score {score_4o}")
        for item in multi_data_list:
            if item["judge_answer"]["score_4o"] == score_4o:
                print(f"Add {item['foldername']} to sample_multi_data")
                sample_multi_data.append(item)
                score_4o_cnt[score_4o] = 1
                break

# 如果3分少于2分的1/5，需要调整
while score_4o_cnt["3"] < score_4o_cnt["2"] // 5:
    print("Warning: Adjust 3 score")
    for item in multi_data_list:
        if item["judge_answer"]["score_4o"] == "3":
            print(f"Add {item['foldername']} to sample_multi_data")
            sample_multi_data.append(item)
            for result in item["test_results"]:
                score_4o = result["judge_answer"]["score_4o"]
                score_4o_cnt[score_4o] += 1
            break
# 再次统计一下4o的分数分布
print("Score 4o distribution after adjustment:")
print(score_4o_cnt)
print()

# for item in sample_multi_data:
#     foldername = item["foldername"]
#     name = item["name"]
#     print(f"Copy {foldername} from {name} to SampleAnalysis/multi")
#     # copy image
#     src_image_dir_path = os.path.join(MULTI_PATH, name, "images", foldername)
#     dst_image_dir_path = os.path.join(SAMPLE_MULTI_PATH, "images", foldername)
#     if not os.path.exists(dst_image_dir_path):
#         os.makedirs(dst_image_dir_path)
#     for image_name in get_immediate_files(src_image_dir_path):
#         src_image_path = os.path.join(src_image_dir_path, image_name)
#         dst_image_path = os.path.join(dst_image_dir_path, image_name)
#         shutil.copyfile(src_image_path, dst_image_path)
# # copy data_multi.json
# sample_multi_data_path = os.path.join(SAMPLE_MULTI_PATH, "sample.json")
# write_json(sample_multi_data_path, sample_multi_data)


# ================== Sample Pure Single ==================
# 读取所有pure_single文件夹下的数据，随机抽取30个放入SampleAnalysis/pure_single文件夹下
# pure_single_name_list = get_immediate_subdirectories(PURE_SINGLE_PATH)
# pure_single_data_list = list()
# pure_single_data_dict = dict()
# perfect_cnt = 0
# for name in pure_single_name_list:
#     data_single_path = os.path.join(PURE_SINGLE_PATH, name, "data_single.json")
#     data_single = read_json(data_single_path)
#     data_single_judge_test_path = os.path.join(
#         TOTAL_RIA_PATH, name, "gpt-4o_test_and_judge.json"
#     )
#     data_single_judge_test = read_json(data_single_judge_test_path)
#     # 合并数据和评测4o结果
#     for item in data_single:
#         foldername = item["foldername"]
#         if foldername not in data_single_judge_test:
#             print(f"Error: {foldername} not in data_single_judge_test")
#             print(f"name: {name}")
#         else:
#             for key in data_single_judge_test[foldername]:
#                 item[key] = data_single_judge_test[foldername][key]
#             if item["judge_answer"]["score_4o"] == "4":
#                 perfect_cnt += 1
#     pure_single_data_list.extend(data_single)
#     sub_single_dict = dict()
#     for item in data_single:
#         item["name"] = name
#         sub_single_dict[item["foldername"]] = item
#     # 检查是否有重复的key
#     if not set(pure_single_data_dict.keys()).isdisjoint(set(sub_single_dict.keys())):
#         # isdisjoint() 方法用于判断两个集合是否包含相同的元素，如果没有返回 True，否则返回 False。
#         print("Warning: Duplicate key in pure_single_data dict")
#         print("Duplicate key is:")
#         for key in set(pure_single_data_dict.keys()).intersection(
#             set(sub_single_dict.keys())
#         ):
#             print(key)
#             print("current name", name)
#             print("before name", pure_single_data_dict[key]["name"])
#     pure_single_data_dict.update(sub_single_dict)

# print(f"Total single images: {len(pure_single_data_list)}")
# print(f"Perfect single images: {perfect_cnt}")
# print()
# # 舍弃perfect的数据
# pure_single_data_list = [
#     item
#     for item in pure_single_data_list
#     if "judge_answer" in item and item["judge_answer"]["score_4o"] != "4"
# ]
# print(f"Non-perfect single images: {len(pure_single_data_list)}")

# # 随机抽取30个
# random.shuffle(pure_single_data_list)
# random.shuffle(pure_single_data_list)
# random.shuffle(pure_single_data_list)
# # random.shuffle() 方法将序列的所有元素随机排，内部使用的是Fisher–Yates shuffle算法
# sample_pure_single_data = pure_single_data_list[:30]
# # 先统计一下4o的分数分布，如果缺少某个分数，需要补充，如果分布不均匀，需要调整
# score_4o_cnt = dict()
# for item in sample_pure_single_data:
#     score_4o = item["judge_answer"]["score_4o"]
#     if score_4o not in score_4o_cnt:
#         score_4o_cnt[score_4o] = 0
#     score_4o_cnt[score_4o] += 1
# print("Score 4o distribution:")
# print(score_4o_cnt)
# print()
# # 补充缺少的分数
# for score_4o in ["0", "1", "2", "3"]:
#     if score_4o not in score_4o_cnt:
#         print(f"Warning: Missing score {score_4o}")
#         for item in pure_single_data_list:
#             if item["judge_answer"]["score_4o"] == score_4o:
#                 print(f"Add {item['foldername']} to sample_pure_single_data")
#                 sample_pure_single_data.append(item)
#                 score_4o_cnt[score_4o] = 1
#                 break
# # 如果3分少于2分的1/5，需要调整
# if score_4o_cnt["3"] < score_4o_cnt["2"] // 5:
#     print("Warning: Adjust 3 score")
#     for item in pure_single_data_list:
#         if item["judge_answer"]["score_4o"] == "3":
#             print(f"Add {item['foldername']} to sample_pure_single_data")
#             sample_pure_single_data.append(item)
#             score_4o_cnt["3"] += 1
#             break
# # 再次统计一下4o的分数分布
# print("Score 4o distribution after adjustment:")
# print(score_4o_cnt)
# print()

# for item in sample_pure_single_data:
#     foldername = item["foldername"]
#     name = item["name"]
#     print(f"Copy {foldername} from {name} to SampleAnalysis/pure_single")
#     # copy image
#     src_image_dir_path = os.path.join(PURE_SINGLE_PATH, name, "images", foldername)
#     dst_image_dir_path = os.path.join(SAMPLE_PURE_SINGLE_PATH, "images", foldername)
#     if not os.path.exists(dst_image_dir_path):
#         os.makedirs(dst_image_dir_path)
#     for image_name in get_immediate_files(src_image_dir_path):
#         src_image_path = os.path.join(src_image_dir_path, image_name)
#         dst_image_path = os.path.join(dst_image_dir_path, image_name)
#         shutil.copyfile(src_image_path, dst_image_path)
# # copy data_single.json
# sample_pure_single_data_path = os.path.join(SAMPLE_PURE_SINGLE_PATH, "sample.json")
# write_json(sample_pure_single_data_path, sample_pure_single_data)
