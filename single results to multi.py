# single results to multi

import json
import os

# MODEL = "claude-3-5-sonnet-20240620"
MODEL_list = [
    "gpt-4o",
    "gemini-1.5-pro-001",
    "gemini-1.5-flash-001",
    "claude-3-5-sonnet-20240620",
    "glm-4v",
    "yi-vision",
    "qwen-vl-max-0809",
    "qwen-vl-plus-0809",
    "chatglm-4v",
    "yi-version",
    "internVL",
    "internlm-xcomposer2d5-7b",
    "VILA1.5-40b",
]
# 需要测试的模型：
# "gpt-4o"
# "gemini-1.5-pro-001"
# "gemini-1.5-flash-001"
# "claude-3-5-sonnet-20240620"

name_list = [
    "djt",
    "fxt",
    "fxx",
    "hzm",
    "kjx",
    "li-rat",
    "lny",
    "rat",
    "wzd",
    "zdw",
    "zql",
]

LOG_FILE_PATH = "./s2m_log.log"


def single_results_to_multi(single_results, multi_results):
    for multi_foldername, multi_result_list in multi_results.items():
        if multi_result_list[0] is None or multi_result_list[0] == "Error":
            if multi_foldername in single_results:
                multi_result_list[0] = single_results[multi_foldername]
            else:
                # print("Error:" + multi_foldername + "Not found in single results!")
                log_to_file(
                    "Error:" + multi_foldername + "Not found in single results!"
                )
    return multi_results


def single_judge_to_multi(single_judge, multi_judge):
    for multi_foldername, multi_judge_list in multi_judge.items():
        if multi_judge_list[0] is None or multi_judge_list[0] == "Error":
            if multi_foldername in single_judge:
                multi_judge_list[0] = single_judge[multi_foldername]
            else:
                # print("Error:" + multi_foldername + "Not found in single judge!")
                log_to_file("Error:" + multi_foldername + "Not found in single judge!")
    return multi_judge


def single_tandj_to_multi(single_tandj, multi_tandj):
    for multi_foldername, multi_tandj_list in multi_tandj.items():
        firstitem = multi_tandj_list[0]
        if ("MLLM_answer" in firstitem and firstitem["MLLM_answer"] is None) or (
            "judge_answer" in firstitem and firstitem["judge_answer"] == "Error"
        ):
            if multi_foldername in single_tandj:
                multi_tandj_list[0] = single_tandj[multi_foldername]
            else:
                # print(
                #     "Error:" + multi_foldername + "Not found in single test and judge!"
                # )
                log_to_file(
                    "Error:" + multi_foldername + "Not found in single test and judge!"
                )
    return multi_tandj


# 将控制台输出日志写入日志文件
def log_to_file(message):
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
        print(message)


if __name__ == "__main__":

    for name in name_list:
        log_to_file("--------------------")
        log_to_file("\nNow processing: " + name)
        # print("--------------------")
        # print("\nNow processing: " + name)
        for MODEL in MODEL_list:
            # print("model: " + MODEL)
            log_to_file("---model: " + MODEL)
            single_path = "./Week1Collection/" + name + "/"
            multi_path = "./Multi_Images/" + name + "/"

            single_results_path = single_path + MODEL + "_results.json"
            multi_results_path = multi_path + MODEL + "_multi_results.json"
            complete_multi_results_path = (
                multi_path + MODEL + "_multi_results_complete.json"
            )

            single_judge_path = single_path + MODEL + "_judge.json"
            multi_judge_path = multi_path + MODEL + "_multi_judge.json"
            complete_multi_judge_path = (
                multi_path + MODEL + "_multi_judge_complete.json"
            )

            single_tandj_path = single_path + MODEL + "_test_and_judge.json"
            multi_tandj_path = multi_path + MODEL + "_multi_test_and_judge.json"
            complete_multi_tandj_path = (
                multi_path + MODEL + "_multi_test_and_judge_complete.json"
            )

            # result==================
            single_results = []
            multi_results = []
            if os.path.exists(single_results_path):
                with open(single_results_path, "r", encoding="utf-8") as f:
                    single_results = json.load(f)
            else:
                log_to_file("Error: " + single_results_path + " not found!")
                continue
            if os.path.exists(multi_results_path):
                with open(multi_results_path, "r", encoding="utf-8") as f:
                    multi_results = json.load(f)
            else:
                log_to_file("Error: " + multi_results_path + " not found!")
                continue

            complete_results = single_results_to_multi(single_results, multi_results)
            with open(complete_multi_results_path, "w", encoding="utf-8") as f:
                json.dump(complete_results, f, ensure_ascii=False, indent=4)
            # print("Complete result!")
            log_to_file("Complete result!")

            # judge==================
            single_judge = []
            multi_judge = []
            if os.path.exists(single_judge_path):
                with open(single_judge_path, "r", encoding="utf-8") as f:
                    single_judge = json.load(f)
            else:
                log_to_file("Error: " + single_judge_path + " not found!")
                continue
            if os.path.exists(multi_judge_path):
                with open(multi_judge_path, "r", encoding="utf-8") as f:
                    multi_judge = json.load(f)
            else:
                log_to_file("Error: " + multi_judge_path + " not found!")
                continue

            complete_judge = single_judge_to_multi(single_judge, multi_judge)
            with open(complete_multi_judge_path, "w", encoding="utf-8") as f:
                json.dump(complete_judge, f, ensure_ascii=False, indent=4)
            # print("Complete judge!")
            log_to_file("Complete judge!")

            # test and judge==================
            single_tandj = []
            multi_tandj = []
            if os.path.exists(single_tandj_path):
                with open(single_tandj_path, "r", encoding="utf-8") as f:
                    single_tandj = json.load(f)
            else:
                log_to_file("Error: " + single_tandj_path + " not found!")
                continue
            if os.path.exists(multi_tandj_path):
                with open(multi_tandj_path, "r", encoding="utf-8") as f:
                    multi_tandj = json.load(f)
            else:
                log_to_file("Error: " + multi_tandj_path + " not found!")
                continue

            complete_tandj = single_tandj_to_multi(single_tandj, multi_tandj)
            with open(complete_multi_tandj_path, "w", encoding="utf-8") as f:
                json.dump(complete_tandj, f, ensure_ascii=False, indent=4)
            # print("Complete test and judge!")
            log_to_file("Complete test and judge!")
