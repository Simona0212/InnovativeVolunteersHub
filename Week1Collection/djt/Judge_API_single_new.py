# Judge_API_single.py

import os
import requests
import json
import time

# =======================
# Configuration
# =======================
API_URL = "https://aigptx.top/v1/chat/completions"
# 可选API_URL：
# "https://cn2us02.opapi.win/v1/chat/completions"
# "https://api.ohmygpt.com/v1/chat/completions"
# "https://cn2us02.opapi.win/v1/chat/completions"
# "https://c-z0-api-01.hash070.com/v1/chat/completions"
# "https://aigptx.top/v1/chat/completions"
# "https://cfwus02.opapi.win/v1/chat/completions"
API_KEY = "sk-Z5VdcIL18691422be52ET3BlBkFJ9bF56d579a444dc79179"  # 请勿改动
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

JUDGE_GROUP_SIZE = 20

SLEEP_TIME = 7  # 单位：秒，控制请求速度，避免触发限制
# 经验值，不代表所有情况，根据实际情况调整
# "gpt-4o-2024-08-06" 最佳SLEEP_TIME=6

TESTMODEL = "gpt-4o"  # 被打分的模型
# 被打分的模型：
# "gpt-4o"
# "gemini-1.5-pro-001"
# "gemini-1.5-flash-001"
# "claude-3-5-sonnet-20240620"
# "yi-vision"
# "glm-4v"

# 不要修改judge法官模型！
MODEL = "gpt-4o-2024-08-06"  # 打分的模型（judge法官）
# 打分的模型："gpt-4o-2024-08-06"

# 请勿改动
PROMPT = """Evaluate the quality of responses provided by MLLMs using the following criteria:
- 4 points: Accurate and logically consistent. Convey the same level of thoughtfulness and insight, the same caliber of intellectual rigor and comprehension with standard answer. (Not required to be literally identical to standard answers)
- 3 points: Shows reasonable understanding but may be incomplete or lack key insights, such as mentioning key facts but failing to effectively summarize the relationship. However, what can be directly got from the images or a common theme with little similarity with the standard answer are not key facts.
- 2 points: Somewhat relevant but lacks depth, is overly broad, or misses critical elements needed for a coherent explanation; does not address or align with the intended standard reasoning at all.
- 1 point: Displays uncertainty, offering vague or incomplete reasoning, or concedes with phrases like "I don't know."
- 0 points: Factuality hallucination in the explanation, i.e. contains factual inaccuracies or fabricated information that undermines its reasoning.

You will receive multiple independent questions in a numbered format:
1. MLLM Output:[] \n Standard Answer: [] \n\n 2. MLLM Output:[] \n Standard Answer: [] \n\n

Provide your response in JSON format where each key is the question number and the value is your answer:
{
    "1": {"score_4o": "",\n"score_reason": ""},
    "2": {"score_4o": "",\n"score_reason": ""},
}

Rating examples:

**Example 1**
MLLM Output:["- **First image**: Chicago skyline with Willis Tower and glass buildings.\n- **Second image**: Cloud Gate ("The Bean") sculpture in Millennium Park.\n- **Relation**: **Chicago landmarks**\n- **Explanation**: Both are iconic Chicago structures - the Willis Tower defining the skyline and Cloud Gate serving as a renowned public sculpture, representing the city's architectural heritage."] \n Standard Answer: ["relation": "Chicago","explanation": "Both Skyscraper and Bean are located in Chicago. Skyscrapers are a prominent feature of Chicago's skyline, and Cloud Gate (\"The Bean\") is a famous public sculpture located in Millennium Park, Chicago.","reasoning": "LocatedIn(Skyscraper, Chicago)\nLocatedIn(Bean, Chicago)\nThus, Skyscraper → Chicago and Bean → Chicago"]\n
{"score_4o": "4",\n"score_reason": "The MLLM's output captures the essence of both images as notable Chicago landmarks, consistent with the standard answer, although its summary 'Chicago landmarks' differs from the standard answer 'Chicago.'"}

**Example 2**
MLLM Output:["- **First image**: Crown of thorns - Christian symbol of suffering.\n- **Second image**: Portrait of Bach, composer of religious music.\n- **Relation**: Religious devotion and expression.\n- **Explanation**: The crown represents Christ's Passion while Bach composed spiritual works like St. Matthew Passion, both expressing Christian themes of suffering and devotion."] \n Standard Answer: ["relation": "St. Matthew Passion", "explanation": "The crown of thorns represents the Passion of Christ, the subject of the work. The portrait of Bach directly connects to the composer of the St. Matthew Passion.","reasoning": "Depict(StMatthewPassion, PassionOfChrist) and Symbolize(CrownOfThorns, PassionOfChrist)\nCompose(Bach, StMatthewPassion)\nThus, CrownOfThorns → PassionOfChrist → StMatthewPassion and Bach → StMatthewPassion"]\n
{"score_4o": "3",\n"score_reason": "The MLLM's output partially captures the relationship but lacks precision. However, it correctly mentions Bach's work 'St. Matthew Passion' which is a key fact consistent with the standard answer."}

**Example 3**
MLLM Output:["- **First image**: Crystal chandelier.\n- **Second image**: White masquerade mask.\n- **Relation**: Elegance and mystery.\n- **Explanation**: The chandelier suggests opulence in theater settings, while the mask represents anonymity at formal events, combining themes of luxury and hidden identities."] \n Standard Answer: ["relation": "The Phantom Of the Opera","explanation": "The white mask is the Phantom's signature disguise, concealing his disfigured face and adding to his mystique. The falling chandelier is a dramatic and iconic scene from the musical, representing the Phantom's power and anger.","reasoning": "Wear(Phantom, Mask) and Character(Phantom, ThePhantomOfTheOpera)\nEvent(FallingChandelier, ThePhantomOfTheOpera)\nThus, Mask → Phantom → ThePhantomOfTheOpera and FallingChandelier → ThePhantomOfTheOpera",]\n
{"score_4o": "2",\n"score_reason": "The concept 'Elegance and mystery' is too broad and it fails to mention any key facts related to 'The Phantom of the Opera'."}

**Example 4**
MLLM Output:["- **First image**: Man in formal attire\n- **Second image**: Plover near water \n- **Relation**: Unknown connection  \n- **Explanation**: No clear connection between the formal portrait and shorebird. Different subjects without obvious relationship."] \n Standard Answer: ["relation": "the origin of the Guinness World Records","explanation": "The Guinness World Records was created by Sir Hugh Beaver, the managing director of the Guinness Brewery. The idea for the book came about when he got into an argument about which was the fastest game bird in Europe, the golden plover or the red grouse, while on a hunting trip.","reasoning": "Create(GuinnessWorldRecords, SirHughBeaver)\nIdeaCameFrom(GuinnessWorldRecords, GoldenPlover)\nThus, SirHughBeaver → GuinnessWorldRecords → GoldenPlover",]\n
{"score_4o": "1",\n"score_reason": "The MLLM expresses uncertainty with 'Unknown connection.'"}

**Example 5**
MLLM Output:["- **First image**: Sanmao comic book cover  \n- **Second image**: Sahara Desert map  \n- **Relation**: Journey  \n- **Explanation**: Sanmao's adventures include stories in the Sahara Desert, connecting the character's travels with the desert setting."] \n Standard Answer: ["relation": "三毛","explanation": "三毛 is a Taiwanese writer who wrote 'The Stories of the Sahara'. The story is about her life in the Sahara Desert. The Sahara map is related to the story. Sanmao is a manhua character created by Zhang Leping in 1935. They share the same name.","reasoning": "WriteBy(三毛, TheStoriesOfSahara) and Related(TheStoriesOfSahara, SaharaMap)\nSameName(三毛, Sanmao)\nThus, SaharaMap → TheStoriesOfSahara → 三毛 → Sanmao"]\n
{"score_4o": "0",\n"score_reason": "The MLLM includes incorrect facts, confusing 'Sanmao' with unrelated adventures in the Sahara Desert. It has confused the facts related to 'Sanmao (comics)' with those of 'Sanmao (writer).'"}"""


# =======================
# 获取当前脚本所在文件夹路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# 使用当前脚本文件夹路径
FOLDER_PATH = os.path.join(BASE_DIR, "img")  # 假设 img 文件夹在当前脚本同一目录下
DATASET_FILE_PATH = os.path.join(BASE_DIR, "labels_test.json")  # 假设 json 文件在当前脚本同一目录下
RESULTS_FILE_PATH = os.path.join(BASE_DIR, f"{TESTMODEL}_results.json")
LOG_FILE_PATH = os.path.join(BASE_DIR, f"{TESTMODEL}_judge.log")
JUDGE_FILE_PATH = os.path.join(BASE_DIR, f"{TESTMODEL}_judge.json")  # 评分结果保存到此JSON文件
COMBINE_FILE_PATH = os.path.join(BASE_DIR, f"{TESTMODEL}_test_and_judge.json")
# =======================


def generate_prompt(data_item, mllm_output):
    relation = data_item["relation"]
    explanation = data_item["explanation"]
    reasoning = data_item["reasoning"]
    user_prompt = f'MLLM Output:{mllm_output} \n Standard Answer: ["relation": "{relation}", "explanation": "{explanation}", "reasoning": "{reasoning}"]'
    return user_prompt


def generate_payload(user_prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": PROMPT,
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                ],
            },
        ],
        "max_tokens": 100 * JUDGE_GROUP_SIZE,
    }
    return payload


def check_json_data_is_judged(json_data, test_result_data, judge_results):
    to_be_judged_data = []
    for item in json_data:
        folder_name = item.get("foldername")
        if not folder_name:
            log_to_file("No foldername specified in JSON item.")
            continue
        # 先检查results文件里是否已经有结果
        if folder_name not in test_result_data:
            log_to_file(f"No test results found for folder: {folder_name}")
            continue
        if (
            test_result_data[folder_name] == "Error"
            or test_result_data[folder_name] == "No response generated."
            or test_result_data[folder_name] == ""
        ):
            log_to_file(f"Error: No response generated for folder: {folder_name}")
            continue
        # 如果已经有打分结果，跳过
        if folder_name in judge_results:
            if (
                "score_4o" in judge_results[folder_name]
                and "score_reason" in judge_results[folder_name]
                and judge_results[folder_name]["score_4o"] in ["0", "1", "2", "3", "4"]
            ):
                log_to_file(f"Judge results already found for folder: {folder_name}")
                continue
        to_be_judged_data.append(item)
    return to_be_judged_data


def judge_model_results(json_data, test_result_data):
    if os.path.exists(JUDGE_FILE_PATH):
        with open(JUDGE_FILE_PATH, "r", encoding="utf-8") as f:
            judge_results = json.load(f)
    else:
        judge_results = {}

    unjudged_data_list = check_json_data_is_judged(
        json_data, test_result_data, judge_results
    )
    # 每次取JUDGE_GROUP_SIZE个数据进行打分
    # 计算需要多少次迭代来处理整个列表
    unjudged_length = len(unjudged_data_list) if unjudged_data_list else 0
    # num_iterations = (unjudged_length + 9) // 10  # 加9是为了向上取整
    # 向上取整
    num_iterations = (unjudged_length + JUDGE_GROUP_SIZE - 1) // JUDGE_GROUP_SIZE
    print(f"Number of iterations: {num_iterations}")
    for i in range(num_iterations):
        start_index = i * JUDGE_GROUP_SIZE
        end_index = start_index + JUDGE_GROUP_SIZE
        sub_list = unjudged_data_list[start_index:end_index]

        group_user_prompt = ""
        folder_name_list = []
        for sub_list_index, item in enumerate(sub_list):
            folder_name = item.get("foldername")
            folder_name_list.append(folder_name)
            # 生成评分提示
            user_prompt = generate_prompt(item, test_result_data[folder_name])
            group_user_prompt += f"{sub_list_index+1}. {user_prompt}\n\n"

        # 生成payload
        payload = generate_payload(group_user_prompt)

        # 发送请求
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            log_to_file(f"HTTP error: {e}")
            for folder_name in folder_name_list:
                judge_results[folder_name] = "Error"
        if response.status_code == 200:
            result = response.json()
            response_text = (
                result.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "No response generated.")
            )
            # print(response_text)
            if response_text.startswith("```json\n"):
                response_text = response_text[7:]  # 去掉开头的 ```json
                response_text = response_text.rstrip("```")  # 去掉结尾的 ```
            # print(response_text)
            # input("Press Enter to continue...")
            response_data = json.loads(response_text)
            for sub_list_index, item in enumerate(sub_list):
                folder_name = item.get("foldername")
                judge_results[folder_name] = response_data[str(sub_list_index + 1)]
                log_to_file(f"Judge results for folder {folder_name} updated")
            # judge_results[folder_name] = response_data
            # log_response(response_data, folder_name)
            # log_to_file(f"Judge results for folder {folder_name} updated.")
        else:
            log_to_file(
                f"Error: Unable to judge for {folder_name_list}, status code: {response.status_code}, error message: {response.text}"
            )
            for folder_name in folder_name_list:
                judge_results[folder_name] = "Error"
            # log_to_file(
            #     f"Error: Unable to judge for folder {folder_name}, judgeid {judgeid}, "
            #     f"status code: {response.status_code}, "
            #     f"error message: {response.text}"
            # )
            # judge_results[folder_name] = "Error"

            # 保存到文件
        with open(JUDGE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(judge_results, f, indent=4, ensure_ascii=False)
        # print(f"Judge results for folder {folder_name} saved.")

        time.sleep(SLEEP_TIME)

    return judge_results


def combine_results_and_judge(test_result_data, judge_results):
    combined_results = {}
    for folder_name, MLLM_answer in test_result_data.items():
        if folder_name not in judge_results:
            log_to_file(f"Warning: Judge results not found for folder: {folder_name}")
            continue
        if (
            MLLM_answer == "Error"
            or MLLM_answer == "No response generated."
            or MLLM_answer == ""
            or MLLM_answer is None
        ):
            log_to_file(f"Warning: MLLM answer not found for folder: {folder_name}")
            continue
        judge_answer = judge_results[folder_name]
        combined_results[folder_name] = {
            "MLLM_answer": MLLM_answer,
            "judge_answer": judge_answer,
        }

    return combined_results


# 将控制台输出日志写入日志文件
def log_to_file(message):
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
        print(message)


# 将 GPT 响应结果写入日志文件
def log_response(response_data, folder_name):
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(f"Folder: {folder_name}\n")
        log_file.write(json.dumps(response_data, indent=4, ensure_ascii=False))
        log_file.write("\n\n")


# =======================
# Main Processing
# =======================
def main():
    if not os.path.exists(DATASET_FILE_PATH):
        print(f"Dataset file not found: {DATASET_FILE_PATH}")
        return

    if not os.path.exists(RESULTS_FILE_PATH):
        print(f"Result file not found: {RESULTS_FILE_PATH}")
        return

    with open(DATASET_FILE_PATH, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    with open(RESULTS_FILE_PATH, "r", encoding="utf-8") as f:
        test_result_data = json.load(f)  # 字典

    if not os.path.exists(JUDGE_FILE_PATH):
        # 如果文件不存在，创建一个空的 JSON 文件
        with open(JUDGE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f)

    judge_results = judge_model_results(json_data, test_result_data)

    # # 将所有结果写入最终的 JSON 文件
    with open(JUDGE_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(judge_results, f, indent=4, ensure_ascii=False)

    log_to_file(f"Finish: Judge results all saved to {JUDGE_FILE_PATH}")

    combined_results = combine_results_and_judge(test_result_data, judge_results)

    with open(COMBINE_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_results, f, indent=4, ensure_ascii=False)

    log_to_file(f"Finish: Combined results all saved to {COMBINE_FILE_PATH}")


if __name__ == "__main__":
    main()
