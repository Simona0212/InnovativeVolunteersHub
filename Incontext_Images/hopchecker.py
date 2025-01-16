import json

name_list = [
    "djt",
    "fxt",
    "ljf",
    "lny",
    "tc",
    "wjl",
    "wzd",
    "zdw",
    "zhb",
]

LOG_FILE_PATH = "./hop_log.log"

path = "./"


# 将控制台输出日志写入日志文件
def log_to_file(message):
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
        print(message)


forbidden_word = set(["first", "second", "third", "fourth"])

for name in name_list:
    with open(path + name + "/data_context.json", "r", encoding="utf-8") as f:
        data_context = json.load(f)  # list
        # data_context_new = data_context[:]
        for item in data_context:
            expla1 = item["reasoning"][0]["explanation"]
            expla2 = item["reasoning"][1]["explanation"]
            if any(word in expla1 for word in forbidden_word) or any(
                word in expla2 for word in forbidden_word
            ):
                log_to_file(name + " " + item["foldername"] + "含有禁用词")
            # cur_hop = item["hop_count"]
            # # 数字符串中→的个数
            # first_hop = item["reasoning"][0]["path"].count("→")
            # second_hop = item["reasoning"][1]["path"].count("→")
            # if first_hop != second_hop:
            #     log_to_file(name + " " + item["foldername"] + "箭头数不相等")
            #     continue
            # elif first_hop != cur_hop:
            #     log_to_file(name + " " + item["foldername"] + "hop_count已修正")
            #     item["hop_count"] = first_hop
            #     with open(
            #         path + name + "/data_context.json", "w", encoding="utf-8"
            #     ) as f:
            #         json.dump(data_context, f, ensure_ascii=False, indent=4)
            #     continue
