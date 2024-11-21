import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # get the directory of this file
INCONTEXT_DIR = os.path.join(
    BASE_DIR, "Incontext_Images"
)  # get the directory of incontext
names_list = ["lny"]
print(names_list)

per_set = set(
    [
        "Visual Similarity",
        "Semantic Object",
        "Contextual Sensory Cues",
        "Scene Contextualization",
        "Abstract Interpretation",
        "Social Insight",
        "Relational Perception",
    ]
)
con_set = set(
    [
        "Functional Links",
        "Causal Connections",
        "Thematic Links",
        "Cultural Reference",
        "Hierarchical Association",
        "Analogical Reasoning",
    ]
)

"""
culture 8个:  
"N/A", 
"USA/English", 
"Non-English European", 
"Latin American", 
"East Asia", 
"Arabic-Islamic", 
"South Asia and South-East Asia", 
"other"
domain 22个: "number", "history", "movie", "cartoon or game", "music", "art", 
"phenomenon", "culture", "ability", "people", "location", "time", "business",
 "sense", "stuff", "myth", "sports", "animal", "food", "country", "city", "STEM"
"""

type_set = set(["metaphor", "relation", "mutual elements"])
culture_set = set(
    [
        "N/A",
        "USA/English",
        "Non-English European",
        "Latin American",
        "East Asia",
        "Arabic-Islamic",
        "South Asia and South-East Asia",
        "other",
    ]
)
domain_set = set(
    [
        "number",
        "history",
        "movie",
        "cartoon or game",
        "music",
        "art",
        "phenomenon",
        "culture",
        "ability",
        "people",
        "location",
        "time",
        "business",
        "sense",
        "stuff",
        "myth",
        "sports",
        "animal",
        "food",
        "country",
        "city",
        "STEM",
    ]
)


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


# incontext_cnt = 0
for name in names_list:
    print("\n" + name)
    data_path = os.path.join(INCONTEXT_DIR, name, "data_context.json")
    data = read_json(data_path)
    data_foldername_set = set()
    for item in data:
        data_foldername_set.add(item["foldername"])
    if len(data_foldername_set) != len(data):
        print("Error: Duplicate foldername in %s!" % name)

    # 检查标签是否正确完成、没有拼写错误
    data_language_set = set()
    # data_copy_map = {}

    data_total = len(data)
    print("total: ", data_total)

    for item in data:
        if "type" not in item:
            print("Error: type is missing in %s!" % item["foldername"])
        elif item["type"] not in type_set:
            print("Error: type label is wrong in %s!" % item["foldername"])
        if "culture" not in item:
            print("Error: culture is missing in %s!" % item["foldername"])
        elif item["culture"] not in culture_set:
            print("Error: culture label is wrong in %s!" % item["foldername"])
        if "domain" not in item:
            print("Error: domain is missing in %s!" % item["foldername"])
        elif isinstance(item["domain"], list) is False or len(item["domain"]) != 2:
            print("Error: domain label is wrong in %s!" % item["foldername"])
        elif item["domain"][0] not in domain_set or item["domain"][1] not in domain_set:
            print("Error: domain label is wrong in %s!" % item["foldername"])
        if "language" not in item:
            print("Error: language is missing in %s!" % item["foldername"])
        else:
            data_language_set.add(item["language"])
        # data_copy_map[item["foldername"]] = item

        path1 = item["reasoning"][0]["path"]
        path2 = item["reasoning"][1]["path"]
        # 检查reasoning是否合理（用\n隔开若干子串，只有最后一个子串可以有→）
        reasoning_list1 = path1.split("\n")
        for i in range(len(reasoning_list1) - 1):
            if "→" in reasoning_list1[i]:
                print("Error: reasoning path 1 is wrong in %s!" % item["foldername"])
        reasoning_list2 = path2.split("\n")
        for i in range(len(reasoning_list2) - 1):
            if "→" in reasoning_list2[i]:
                print("Error: reasoning path 2 is wrong in %s!" % item["foldername"])
        if path1.count("→") != path2.count("→"):
            print("Error: hop count is different in %s!" % item["foldername"])
        else:
            if item["hop_count"] != path1.count("→"):
                item["hop_count"] = path1.count("→")
                write_json(data_path, data)
                print("Update hop count in %s!" % item["foldername"])

print("Done!")
