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

SLEEP_TIME = 7  # 单位：秒，控制请求速度，避免触发限制
# 经验值，不代表所有情况，根据实际情况调整
# "gpt-4o-2024-08-06" 最佳SLEEP_TIME=6

TESTMODEL = "VILA1.5-40b"  # 被打分的模型
# 被打分的模型：
# "gpt-4o"
# "gemini-1.5-pro-001"
# "gemini-1.5-flash-001"
# "claude-3-5-sonnet-20240620"

# 不要修改judge法官模型！
MODEL = "gpt-4o-2024-08-06"  # 打分的模型（judge法官）
# 打分的模型："gpt-4o-2024-08-06"

# 请勿改动
PROMPT = """Please act as an impartial judge and evaluate the quality of the responses provided by MLLMs. Score the MLLM outputs according to the following scoring criteria and compare the "relation", "explanation" and "reasoning" with the standard answers:
- 4 points: Exactly correct and consistent in meaning with the standard answer (Not required to be literally identical to standard answers, but should convey the same level of thoughtfulness and insight, the same caliber of intellectual rigor and comprehension.)
- 3 points: Roughly correct, similar with the standard answer but incomplete, such as mentioning key facts but failing to effectively summarize the relationship. However, key facts that can be directly got from the images are usually excluded. A common theme with little similarity with the standard answer is not a key fact.
- 2 points: Roughly correct but too broad, without relevant facts in the standard answer; not related to the standard answer; does not address or align with the intended standard reasoning at all.
- 1 point: Responds with 'I don't know,' 'I can't help,' 'Unknown connection,' etc., or expresses its uncertainty cautiously.
- 0 points: Factuality hallucination in the explanation, i.e. contains erroneous information or fabricated content. (Note that hallucination is only related to the MLLM's explanation. That is, even if MLLM's answer does not does not, it must not get 0 points unless it refers to erroneous information. Divergent opinions on the image theme do not lead to factual hallucination, but wrong image content does.)

Input Format:
MLLM Output:[] \n Standard Answer: []

Please refer to the above scoring criteria carefully when evaluating the MLLM output and assign a score based on the actual response. Please format the output as follows:
{"score_4o": "",\n"score_reason": ""}

Rating examples:

**Example 1**
MLLM Output:["- **First image**: A cityscape featuring tall skyscrapers, including a prominent black tower and a glass-covered building.\n- **Second image**: A famous public sculpture, \"Cloud Gate\" (also known as \"The Bean\"), surrounded by modern city buildings.\n- **Relation**: **Chicago landmarks**\n- **Explanation**: Both images depict iconic views of Chicago. The first image highlights the city's skyline, including the Willis Tower (formerly Sears Tower), while the second image shows Cloud Gate, a renowned sculpture in Millennium Park. Both elements are central to Chicago’s urban identity and architectural significance.\n"] \n Standard Answer: ["relation": "Chicago","explanation": "Both Skyscraper and Bean are located in Chicago. Skyscrapers are a prominent feature of Chicago's skyline, and Cloud Gate (\"The Bean\") is a famous public sculpture located in Millennium Park, Chicago.","reasoning": "LocatedIn(Skyscraper, Chicago)\nLocatedIn(Bean, Chicago)\nThus, Skyscraper → Chicago and Bean → Chicago"]\n
{"score_4o": "4",\n"score_reason": "The MLLM's output summarizes the relationship as 'Chicago landmarks.' Although this differs from the standard answer 'Chicago,' it accurately captures the essence of both images—depicting the Skyscraper and the Bean—as they are indeed notable landmarks located in Chicago."}

**Example 2**
MLLM Output:["- **First image**: A crown of thorns, a symbol associated with suffering and sacrifice, particularly in the context of Christian theology.\n- **Second image**: A portrait of a man, likely Johann Sebastian Bach, a renowned composer known for his sacred music.\n- **Relation**: Religious devotion and expression.\n- **Explanation**: The crown of thorns symbolizes sacrifice, pain, and religious significance, particularly relating to the Passion of Christ. Bach, known for his deeply spiritual compositions, including works such as the *St. Matthew Passion*, used music as a means of expressing and reflecting on Christian themes of suffering, redemption, and devotion. Together, these images highlight the intersection between physical symbols of faith and artistic expression that conveys spiritual depth and reverence.\n"] \n Standard Answer: ["relation": "St. Matthew Passion", "explanation": "The crown of thorns represents the Passion of Christ, the subject of the work. The portrait of Bach directly connects to the composer of the St. Matthew Passion.","reasoning": "Depict(StMatthewPassion, PassionOfChrist) and Symbolize(CrownOfThorns, PassionOfChrist)\nCompose(Bach, StMatthewPassion)\nThus, CrownOfThorns → PassionOfChrist → StMatthewPassion and Bach → StMatthewPassion"]\n
{"score_4o": "3",\n"score_reason": "The MLLM's output summarizes the relationship between 'A crown of thorns' and Bach as 'Religious devotion and expression,' which is partially correct but does not pinpoint the most precise connection. However, it correctly mentions Bach's work 'St. Matthew Passion' in the explanation, which is a fact consistent with the standard answer."}

**Example 3**
MLLM Output:["- **First image**: A luxurious crystal chandelier with ornate, sparkling details.\n- **Second image**: A plain white masquerade mask, covering only the eyes and nose.\n- **Relation**: Elegance and mystery.\n- **Explanation**: The chandelier represents elegance, grandeur, and opulence, often seen in lavish settings such as ballrooms or theaters. The masquerade mask evokes mystery, intrigue, and anonymity, commonly associated with formal events like masquerade balls. Together, these images suggest a scene of sophisticated, high-society gatherings where beauty and secrecy intertwine, evoking themes of hidden identities and refined aesthetics.\n"] \n Standard Answer: ["relation": "The Phantom Of the Opera","explanation": "The white mask is the Phantom's signature disguise, concealing his disfigured face and adding to his mystique. The falling chandelier is a dramatic and iconic scene from the musical, representing the Phantom's power and anger.","reasoning": "Wear(Phantom, Mask) and Character(Phantom, ThePhantomOfTheOpera)\nEvent(FallingChandelier, ThePhantomOfTheOpera)\nThus, Mask → Phantom → ThePhantomOfTheOpera and FallingChandelier → ThePhantomOfTheOpera",]\n
{"score_4o": "2",\n"score_reason": "The MLLM's output summarizes the concept as 'Elegance and mystery,' which appears to be too broad. Additionally, it fails to mention any facts related to 'The Phantom of the Opera' that would align with the standard answer."}

**Example 4**
MLLM Output:["- **First image**: Portrait of a man in formal attire  \n- **Second image**: A shorebird standing near water (likely a plover)  \n- **Relation**: Unknown connection  \n- **Explanation**: The two images do not appear to have an obvious or direct connection. The first shows a man in a formal setting, while the second image features a bird near a shoreline. Without further context, these two images represent different subjects: one human, one avian, likely from unrelated domains (perhaps history or politics in the first image and nature or ornithology in the second).\n"] \n Standard Answer: ["relation": "the origin of the Guinness World Records","explanation": "The Guinness World Records was created by Sir Hugh Beaver, the managing director of the Guinness Brewery. The idea for the book came about when he got into an argument about which was the fastest game bird in Europe, the golden plover or the red grouse, while on a hunting trip.","reasoning": "Create(GuinnessWorldRecords, SirHughBeaver)\nIdeaCameFrom(GuinnessWorldRecords, GoldenPlover)\nThus, SirHughBeaver → GuinnessWorldRecords → GoldenPlover",]\n
{"score_4o": "1",\n"score_reason": "The MLLM responds with 'Unknown connection,' stating that 'The two images do not appear to have an obvious or direct connection,' and uses words like 'perhaps' to express its uncertainty."}

**Example 5**
MLLM Output:["- **First image**: Cover of a \"Sanmao\" comic book  \n- **Second image**: Map of the Sahara Desert  \n- **Relation**: Journey  \n- **Explanation**: The first image depicts \"Sanmao,\" a famous Chinese comic character known for his travels and adventures. The second image is of the Sahara Desert, which is significant because Sanmao's adventures include stories set in this vast desert. Both images evoke themes of exploration and wandering, with Sanmao's character often experiencing hardship and survival, much like one would in the harsh environment of the Sahara Desert.\n"] \n Standard Answer: ["relation": "三毛","explanation": "三毛 is a Taiwanese writer who wrote 'The Stories of the Sahara'. The story is about her life in the Sahara Desert. The Sahara map is related to the story. Sanmao is a manhua character created by Zhang Leping in 1935. They share the same name.","reasoning": "WriteBy(三毛, TheStoriesOfSahara) and Related(TheStoriesOfSahara, SaharaMap)\nSameName(三毛, Sanmao)\nThus, SaharaMap → TheStoriesOfSahara → 三毛 → Sanmao"]\n
{"score_4o": "0",\n"score_reason": "The MLLM includes incorrect facts in its response. In reality, 'Sanmao (comics)' is famous for depicting the tragic fate of impoverished children and is not directly related to travels and adventures, nor is it associated with the Sahara Desert. The MLLM has confused the facts related to 'Sanmao (comics)' with those of 'Sanmao (writer).'"}"""


FOLDER_PATH = "./"
DATASET_FILE_PATH = "./labels_test.json"
RESULTS_FILE_PATH = "./" + TESTMODEL + "_results" + ".json"  # 将结果保存到此JSON文件
JUDGE_FILE_PATH = "./" + TESTMODEL + "_judge" + ".json"  # 评分结果保存到此JSON文件
LOG_FILE_PATH = "./" + TESTMODEL + "_judge" + ".log"
COMBINE_FILE_PATH = "./" + TESTMODEL + "_test_and_judge" + ".json"
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
        "max_tokens": 300,
    }
    return payload


def judge_model_results(json_data, test_result_data):
    if os.path.exists(JUDGE_FILE_PATH):
        with open(JUDGE_FILE_PATH, "r", encoding="utf-8") as f:
            judge_results = json.load(f)
    else:
        judge_results = {}

    for item in json_data:
        folder_name = item.get("foldername")
        if not folder_name:
            # print("No foldername specified in JSON item.")
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

        # 生成评分提示
        user_prompt = generate_prompt(item, test_result_data[folder_name])
        # 生成payload
        payload = generate_payload(user_prompt)

        # 发送请求
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            log_to_file(f"HTTP error: {e}")
            judge_results[folder_name] = "Error"
        if response.status_code == 200:
            result = response.json()
            response_text = (
                result.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "No response generated.")
            )
            response_data = json.loads(response_text)
            judge_results[folder_name] = response_data
            log_response(response_data, folder_name)
            log_to_file(f"Judge results for folder {folder_name} updated.")
        else:
            log_to_file(
                f"Error: Unable to judge for folder {folder_name}, judgeid {judgeid}, "
                f"status code: {response.status_code}, "
                f"error message: {response.text}"
            )
            judge_results[folder_name] = "Error"

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
