import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # get the directory of this file
TOTAL_RIA_PATH = os.path.join(BASE_DIR, "Week1Collection")
MULTI_PATH = os.path.join(BASE_DIR, "Multi_Images")
PURE_SINGLE_PATH = os.path.join(BASE_DIR, "Pure_Single_Images")
names_list = ["hzm", "rat"]
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


multi_cnt = 0  # multi（扩充）总数
single_cnt = 0  # 纯single数据量
base_cnt = 0
for name in names_list:
    print("\n" + name)
    data_path = os.path.join(TOTAL_RIA_PATH, name, "labels_test.json")
    data = read_json(data_path)
    data_foldername_set = set()
    for item in data:
        data_foldername_set.add(item["foldername"])
    if len(data_foldername_set) != len(data):
        print("Error: Duplicate foldername in %s!" % name)

    # 检查标签是否正确完成、没有拼写错误
    data_language_set = set()
    data_copy_map = {}

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
        elif item["domain"] not in domain_set:
            print("Error: domain label is wrong in %s!" % item["foldername"])
        if "language" not in item:
            print("Error: language is missing in %s!" % item["foldername"])
        else:
            data_language_set.add(item["language"])
        data_copy_map[item["foldername"]] = item

        hop_count = item["hop_count"]
        true_hop_count = item["reasoning"].count("→")
        if hop_count != true_hop_count:
            print("Error: hop_count is wrong in %s!" % item["foldername"])

    print(name, "language: ", data_language_set)

    print("-----single-----")
    single_total = 0
    single_path = os.path.join(PURE_SINGLE_PATH, name)
    if os.path.exists(single_path):
        data_single_path = os.path.join(single_path, "data_single.json")
        data_single_img_path = os.path.join(single_path, "images")
        data_single = read_json(data_single_path)
        # print(name, "pure single len: ", len(data_single))
        # 检查文件夹名是否有改变、pc标签是否正确完成
        single_total = len(data_single)
        for single_item in data_single:
            single_foldername = single_item["foldername"]
            if single_foldername not in data_foldername_set:
                print("Error: %s not in %s!" % (single_foldername, name))
            if "perception" not in single_item:
                print(
                    "Error: perception is missing in %s, %s!"
                    % (single_foldername, name)
                )
            else:
                if (
                    set(single_item["perception"]).issubset(per_set)
                    and len(single_item["perception"]) <= 5
                ):
                    pass
                else:
                    print("Error: perception label is wrong in %s!" % single_foldername)
            if "conception" not in single_item:
                print(
                    "Error: conception is missing in %s, %s!"
                    % (single_foldername, name)
                )
            else:
                if (
                    # single_item["conception"] != []
                    # and
                    set(single_item["conception"]).issubset(con_set)
                    and len(single_item["conception"]) <= 5
                ):
                    pass
                else:
                    print(
                        "Error: conception label is wrong in %s, %s!"
                        % (single_foldername, name)
                    )
            # 检查reasoning是否合理（用\n隔开若干子串，只有最后一个子串可以有→）
            reasoning = single_item["reasoning"]
            reasoning_list = reasoning.split("\n")
            for i in range(len(reasoning_list) - 1):
                if "→" in reasoning_list[i]:
                    print("Error: reasoning is wrong in %s!" % single_foldername)

            # 检查copy是否正确
            cop = data_copy_map[single_foldername]
            if cop["type"] != single_item["type"]:
                if name in names_list:
                    single_item["type"] = cop["type"]
                    write_json(data_single_path, data_single)
                    print("Type is updated in %s!" % single_foldername)
                else:
                    print("Error: %s type not match!" % single_foldername)
            if cop["culture"] != single_item["culture"]:
                print("Error: %s culture not match!" % single_foldername)
            if cop["domain"] != single_item["domain"]:
                print("Error: %s domain not match!" % single_foldername)
            if cop["language"] != single_item["language"]:
                print("Error: %s language not match!" % single_foldername)
            if cop["images"] != single_item["images"]:  # 列表比较、字典比较
                print("Error: %s images not match!" % single_foldername)
            if cop["relation"] != single_item["relation"]:
                if name in names_list:
                    single_item["relation"] = cop["relation"]
                    write_json(data_single_path, data_single)
                    print("Relation is updated in %s!" % single_foldername)
                else:
                    print("Error: %s relation not match!" % single_foldername)
            if cop["explanation"] != single_item["explanation"]:
                if name in names_list:
                    single_item["explanation"] = cop["explanation"]
                    write_json(data_single_path, data_single)
                    print("Explanation is updated in %s!" % single_foldername)
                else:
                    print("Error: %s explanation not match!" % single_foldername)
            if cop["reasoning"] != single_item["reasoning"]:
                if name in names_list:
                    single_item["reasoning"] = cop["reasoning"]
                    write_json(data_single_path, data_single)
                    print("Reasoning is updated in %s!" % single_foldername)
                else:
                    print("Error: %s reasoning not match!" % single_foldername)
            if "hop_count" not in cop:
                print("Error: hop_count is missing in %s!" % single_foldername)
                # break
            elif "hop_count" not in single_item:
                if name in names_list:
                    single_item["hop_count"] = cop["hop_count"]
                    write_json(data_single_path, data_single)
                    print("Hop_count is updated in %s!" % single_foldername)
                else:
                    print("Error: %s hop_count not match!" % single_foldername)
            elif cop["hop_count"] != single_item["hop_count"]:
                if name in names_list:
                    single_item["hop_count"] = cop["hop_count"]
                    write_json(data_single_path, data_single)
                    print("Hop_count is updated in %s!" % single_foldername)
                else:
                    print("Error: %s hop_count not match!" % single_foldername)

        # 检查文件路径和文件夹名是否一一对应
        if os.path.exists(data_single_img_path):
            foldername_list = get_immediate_subdirectories(data_single_img_path)
            for folder in foldername_list:
                if folder not in data_foldername_set:
                    print("Error: %s not in %s!" % (folder, name))
            if len(foldername_list) != len(data_single):
                print("Error: %s single folder number not match!" % name)
                print("foldername_list: ", len(foldername_list))
                print("data_single: ", len(data_single))
                # print("data_foldername_set: ", len(data_foldername_set))
            for single_item in data_single:
                single_foldername = single_item["foldername"]
                if single_foldername not in foldername_list:
                    print(
                        "Error: %s not in %s!"
                        % (single_foldername, data_single_img_path)
                    )
                if os.path.exists(
                    os.path.join(data_single_img_path, single_foldername)
                ):
                    img_list = single_item["images"]
                    for img in img_list:
                        img_name = img["filename"]
                        if not os.path.exists(
                            os.path.join(
                                data_single_img_path, single_foldername, img_name
                            )
                        ):
                            print(
                                "Error: %s not exists in %s!"
                                % (
                                    img_name,
                                    os.path.join(
                                        data_single_img_path, single_foldername
                                    ),
                                )
                            )
                    real_img_list = get_immediate_files(
                        os.path.join(data_single_img_path, single_foldername)
                    )
                    if len(real_img_list) != len(img_list):
                        print(
                            "Error: %s single img number not match!" % single_foldername
                        )
        else:
            print("Error: %s not exists!" % data_single_img_path)
        single_cnt += len(data_single)
    else:
        print("Error: %s not exists!" % single_path)

    print("-----multi-----")
    multi_total = 0
    multi_path = os.path.join(MULTI_PATH, name)
    if os.path.exists(multi_path):
        data_multi_path = os.path.join(multi_path, "data_multi.json")
        data_multi_img_path = os.path.join(multi_path, "images")
        data_multi = read_json(data_multi_path)
        multi_total = len(data_multi)
        # print(name, "multi len: ", len(data_multi))
        counts_total = 0
        for item in data_multi:
            img_list = item["images"]
            cnt1 = img_list[0]["count"]
            cnt2 = img_list[1]["count"]
            total_cnt = cnt1 * cnt2
            counts_total += total_cnt
        # print(name, "multi img cnt: ", counts_total)
        multi_cnt += counts_total
        # print(name, "multi len: ", counts_total)
        # 检查文件夹名是否有改变、pc标签是否正确完成
        for multi_item in data_multi:
            multi_foldername = multi_item["foldername"]
            if multi_foldername not in data_foldername_set:
                print("Error: %s not in %s!" % (multi_foldername, name))
            if "perception" not in multi_item:
                print(
                    "Error: perception is missing in %s, %s!" % (multi_foldername, name)
                )
            else:
                if (
                    set(multi_item["perception"]).issubset(per_set)
                    and len(multi_item["perception"]) <= 5
                ):
                    pass
                else:
                    print("Error: perception label is wrong in %s!" % multi_foldername)
            if "conception" not in multi_item:
                print(
                    "Error: conception is missing in %s, %s!" % (multi_foldername, name)
                )
            else:
                if (
                    multi_item["conception"] != []
                    and set(multi_item["conception"]).issubset(con_set)
                    and len(multi_item["conception"]) <= 5
                ):
                    pass
                else:
                    print(
                        "Error: conception label is wrong in %s, %s!"
                        % (multi_foldername, name)
                    )
            # 检查reasoning是否合理（用\n隔开若干子串，只有最后一个子串可以有→）
            reasoning = multi_item["reasoning"]
            reasoning_list = reasoning.split("\n")
            for i in range(len(reasoning_list) - 1):
                if "→" in reasoning_list[i]:
                    print("Error: reasoning is wrong in %s!" % multi_foldername)

            # 检查copy是否正确
            cop = data_copy_map[multi_foldername]
            if cop["type"] != multi_item["type"]:
                if name in names_list:
                    multi_item["type"] = cop["type"]
                    write_json(data_multi_path, data_multi)
                    print("Type is updated in %s!" % multi_foldername)
                else:
                    print("Error: %s type not match!" % multi_foldername)
            if cop["culture"] != multi_item["culture"]:
                print("Error: %s culture not match!" % multi_foldername)
            if cop["domain"] != multi_item["domain"]:
                print("Error: %s domain not match!" % multi_foldername)
            if cop["language"] != multi_item["language"]:
                print("Error: %s language not match!" % multi_foldername)
            if (
                cop["images"][0]["filename"] != multi_item["images"][0]["filename"]
                or cop["images"][1]["filename"] != multi_item["images"][1]["filename"]
                or cop["images"][0]["description"]
                != multi_item["images"][0]["description"]
                or cop["images"][1]["description"]
                != multi_item["images"][1]["description"]
            ):  # 列表比较、字典比较
                print("Error: %s images not match!" % multi_foldername)
            if cop["relation"] != multi_item["relation"]:
                if name in names_list:
                    multi_item["relation"] = cop["relation"]
                    write_json(data_multi_path, data_multi)
                    print("Relation is updated in %s!" % multi_foldername)
                else:
                    print("Error: %s relation not match!" % multi_foldername)
            if cop["explanation"] != multi_item["explanation"]:
                if name in names_list:
                    multi_item["explanation"] = cop["explanation"]
                    write_json(data_multi_path, data_multi)
                    print("Explanation is updated in %s!" % multi_foldername)
                else:
                    print("Error: %s explanation not match!" % multi_foldername)
            if cop["reasoning"] != multi_item["reasoning"]:
                if name in names_list:
                    multi_item["reasoning"] = cop["reasoning"]
                    write_json(data_multi_path, data_multi)
                    print("Reasoning is updated in %s!" % multi_foldername)
                else:
                    print("Error: %s reasoning not match!" % multi_foldername)
            if "hop_count" not in cop:
                print("Error: hop_count is missing in %s!" % multi_foldername)
                # break
            elif "hop_count" not in multi_item:
                if name in names_list:
                    multi_item["hop_count"] = cop["hop_count"]
                    write_json(data_multi_path, data_multi)
                    print("Hop_count is updated in %s!" % multi_foldername)
                else:
                    print("Error: hop_count is missing in %s!" % multi_foldername)
            elif cop["hop_count"] != multi_item["hop_count"]:
                if name in names_list:
                    multi_item["hop_count"] = cop["hop_count"]
                    write_json(data_multi_path, data_multi)
                    print("Hop_count is updated in %s!" % multi_foldername)
                else:
                    print("Error: %s hop_count not match!" % multi_foldername)

        # 检查文件路径和文件夹名是否一一对应
        if os.path.exists(data_multi_img_path):
            foldername_list = get_immediate_subdirectories(data_multi_img_path)
            for folder in foldername_list:
                if folder not in data_foldername_set:
                    print("Error: %s not in %s!" % (folder, name))
            if len(foldername_list) != len(data_multi):
                print("Error: %s multi folder number not match!" % name)
                print("foldername_list: ", len(foldername_list))
                print("data_multi: ", len(data_multi))
                # print("data_foldername_set: ", len(data_foldername_set))
            for multi_item in data_multi:
                multi_foldername = multi_item["foldername"]
                if multi_foldername not in foldername_list:
                    print(
                        "Error: %s not in %s!" % (multi_foldername, data_multi_img_path)
                    )
                if os.path.exists(os.path.join(data_multi_img_path, multi_foldername)):
                    img_list = multi_item["images"]
                    for img in img_list:
                        img_name = img["filename"]
                        img_count = img["count"]
                        img_name_list = [
                            str(i) + "_" + img_name for i in range(1, img_count + 1)
                        ]
                        for img_name in img_name_list:
                            if not os.path.exists(
                                os.path.join(
                                    data_multi_img_path, multi_foldername, img_name
                                )
                            ):
                                print(
                                    "Error: %s not exists in %s!"
                                    % (
                                        img_name,
                                        os.path.join(
                                            data_multi_img_path, multi_foldername
                                        ),
                                    )
                                )
                    counts_sum = img_list[0]["count"] + img_list[1]["count"]
                    real_img_list = get_immediate_files(
                        os.path.join(data_multi_img_path, multi_foldername)
                    )
                    if len(real_img_list) != counts_sum:
                        print(
                            "Error: %s multi img number not match! %s"
                            % (multi_foldername, name)
                        )
        else:
            print("Error: %s not exists!" % data_multi_img_path)

    base_cnt += data_total
    if data_total != (single_total + multi_total):
        print("Error: wrong total cnt %s" % name)
    print("single: ", single_total)
    print("multi: ", multi_total)
    print("total: ", data_total)

print()
print("multi:", multi_cnt)
print("single:", single_cnt)
print("base:", base_cnt)
