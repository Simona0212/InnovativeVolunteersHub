# single results to multi

import json

MODEL = "claude-3-5-sonnet-20240620"
# 需要测试的模型：
# "gpt-4o"
# "gemini-1.5-pro-001"
# "gemini-1.5-flash-001"
# "claude-3-5-sonnet-20240620"

single_path = "./single/"
multi_path = "./multi/"

single_results_path = single_path + MODEL + "_results.json"
multi_results_path = multi_path + MODEL + "_multi_results.json"
complete_multi_results_path = multi_path + MODEL + "_multi_results_complete.json"

single_judge_path = single_path + MODEL + "_judge.json"
multi_judge_path = multi_path + MODEL + "_multi_judge.json"
complete_multi_judge_path = multi_path + MODEL + "_multi_judge_complete.json"

single_tandj_path = single_path + MODEL + "_test_and_judge.json"
multi_tandj_path = multi_path + MODEL + "_multi_test_and_judge.json"
complete_multi_tandj_path = multi_path + MODEL + "_multi_test_and_judge_complete.json"


def single_results_to_multi(single_results, multi_results):
    for multi_foldername, multi_result_list in multi_results.items():
        if multi_result_list[0] is None or multi_result_list[0] == "Error":
            if multi_foldername in single_results:
                multi_result_list[0] = single_results[multi_foldername]
            else:
                print("Error:" + multi_foldername + "Not found in single results!")
    return multi_results


def single_judge_to_multi(single_judge, multi_judge):
    for multi_foldername, multi_judge_list in multi_judge.items():
        if multi_judge_list[0] is None or multi_judge_list[0] == "Error":
            if multi_foldername in single_judge:
                multi_judge_list[0] = single_judge[multi_foldername]
            else:
                print("Error:" + multi_foldername + "Not found in single judge!")
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
                print(
                    "Error:" + multi_foldername + "Not found in single test and judge!"
                )

    return multi_tandj


if __name__ == "__main__":
    single_results = []
    multi_results = []
    with open(single_results_path, "r", encoding="utf-8") as f:
        single_results = json.load(f)
    with open(multi_results_path, "r", encoding="utf-8") as f:
        multi_results = json.load(f)
    complete_results = single_results_to_multi(single_results, multi_results)
    with open(complete_multi_results_path, "w", encoding="utf-8") as f:
        json.dump(complete_results, f, ensure_ascii=False, indent=4)
    print("Complete result!")

    single_judge = []
    multi_judge = []
    with open(single_judge_path, "r", encoding="utf-8") as f:
        single_judge = json.load(f)
    with open(multi_judge_path, "r", encoding="utf-8") as f:
        multi_judge = json.load(f)
    complete_judge = single_judge_to_multi(single_judge, multi_judge)
    with open(complete_multi_judge_path, "w", encoding="utf-8") as f:
        json.dump(complete_judge, f, ensure_ascii=False, indent=4)
    print("Complete judge!")

    single_tandj = []
    multi_tandj = []
    with open(single_tandj_path, "r", encoding="utf-8") as f:
        single_tandj = json.load(f)
    with open(multi_tandj_path, "r", encoding="utf-8") as f:
        multi_tandj = json.load(f)
    complete_tandj = single_tandj_to_multi(single_tandj, multi_tandj)
    with open(complete_multi_tandj_path, "w", encoding="utf-8") as f:
        json.dump(complete_tandj, f, ensure_ascii=False, indent=4)
    print("Complete test and judge!")
