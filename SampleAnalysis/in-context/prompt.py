import json
import os


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
sample_path = os.path.join(BASE_DIR, "sample.json")  # get the directory of sample
sample_data = read_json(sample_path)  # read the sample data

prompt_data = list()
for sample in sample_data:
    prompt_data.append(
        {
            "data_uid": sample["foldername"],
            "Question": {
                "Image 1 Description": sample["images"][0]["description"],
                "Image 2 Description": sample["images"][1]["description"],
            },
            "Standard Answer": {
                "Relation": sample["relation"],
                "Reasoning Path": sample["reasoning"],
                "Explanation": sample["explanation"],
            },
            "MLLM's Answer": sample["MLLM_answer"],
            "Judge": sample["judge_answer"],
            "Data Labels": {
                "Type of Relationship": sample["type"],
                "Perceptual Association L-3": sample["perception"],
                "Conceptual Association L-3": sample["conception"],
                "Topic Domain": sample["domain"],
                "Culture": sample["culture"],
                "Language of Relation Description": sample["language"],
            },
        }
    )

prompt_path = os.path.join(BASE_DIR, "prompt.json")
write_json(prompt_path, prompt_data)
print("Done!")
