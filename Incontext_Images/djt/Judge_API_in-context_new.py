# Judge_API_in-context_new.py

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

JUDGE_GROUP_SIZE = 20  # 每次评分的数量，根据实际情况调整

SLEEP_TIME = 7  # 单位：秒，控制请求速度（太快了会报错、被封IP）
# 经验值，不代表所有情况，根据实际情况调整
# "gpt-4o-2024-08-06" 最佳SLEEP_TIME=6

TESTMODEL = "gemini-1.5-pro-001"  # 被打分的模型
# 被打分的模型：
# "gpt-4o"
# "gemini-1.5-pro-001"
# "gemini-1.5-flash-001"
# "claude-3-5-sonnet-20240620"

# 不要修改judge法官模型！
MODEL = "gpt-4o-2024-08-06"  # 打分的模型（judge法官）
# 打分的模型："gpt-4o-2024-08-06"

# 请勿改动
PROMPT = """Background:
MLLMs analyze three images, identify relationships between Images 1 and 2, and propose Image 4 that maintains the same relationship with Image 3.

Your task:
Evaluate MLLM responses focusing on Image 4 description, Relation, and Explanation against standard answers using these criteria:

- 4 points: Accurate and logically consistent. Correctly matches standard answer's logic (not necessarily identical). Accurate relation identification and logical Image 4 description.
- 3 points: Generally correct but incomplete. Shows reasonable understanding but may be incomplete or lack key insights, such as mentioning key facts but failing to effectively summarize the relationship.
- 2 points: Somewhat reasonable but lacks depth, is overly broad, or misses critical elements needed for a coherent explanation; does not address or align with the intended standard reasoning at all; completely unrelated to the standard answer's focus; completely misses the thematic connection; does not address the intended theme; a completely different interpretation. Vague relation or loose connection between image 3 and 4.
- 1 point: Responds with 'I don't know,' 'I can't help,' 'Unknown connection,' etc., or expresses its uncertainty cautiously.
- 0 points: Contains factual errors or illogical content. Factuality hallucination in the explanation, i.e. contains factual inaccuracies or fabricated information that undermines its reasoning. (Note that hallucination is only related to the MLLM's explanation. That is, even if MLLM's answer does not address or align with the intended standard reasoning at all, it must not get 0 points unless it refers to erroneous information. Divergent opinions on the image theme do not lead to factual hallucination, but wrong image content does.)

You will receive multiple independent questions in a numbered format:
1. MLLM Output:[] \n Standard Answer: [] \n\n 2. MLLM Output:[] \n Standard Answer: [] \n\n

Provide your response in JSON format where each key is the question number and the value is your answer:
{
    "1": {"score_4o": "",\n"score_reason": ""},
    "2": {"score_4o": "",\n"score_reason": ""}
}

Rating examples:

**Example 1**
MLLM Output:["- **Image 1**: film Amélie\n- **Image 2**: Eiffel Tower\n- **Image 3**: From Vegas to Macau II\n- **Image 4**: Macau Tower\n- **Relation**: Setting/Location\n- **Explanation**: Image 1 (Amélie) is closely tied to Paris, France, where the film was set and shot. Image 2 shows the Eiffel Tower, a symbol of Paris. Likewise, Image 3 (From Vegas to Macau II) highlights Macau in both its title and visuals. Thus, Image 4 should feature a notable Macau landmark, such as the Macau Tower.\n"] \n Standard Answer: ["Image 4": "the new Lisboa Hotel", "relation": "Films Associated with Iconic Locations", "explanation": "Amélie is a film that captures the essence of Paris, showcasing its charm, streets, and culture. Similarly, From Vegas to Macau (澳门风云) is centered around the gambling and nightlife culture in Macau, with the New Lisboa Hotel being a significant landmark in that context.", "reasoning path 1": "FilmSetting(Amelie, Paris)\nCulturalSymbol(EiffelTower, Paris)\nThus, Amelie → Paris", "reasoning path 2": "FilmSetting(MacauStorm, Macau)\nCulturalSymbol(NewLisboaHotel, Macau)\nThus, MacauStorm → NewLisboaHotel"]
{"score_4o": "4","score_reason": "The MLLM accurately linked 'Amélie' with Paris via the Eiffel Tower and 'From Vegas to Macau II' with Macau via the Macau Tower. Although the standard answer highlighted the New Lisboa Hotel for Macau, the Macau Tower is also a valid and recognizable symbol. The MLLM's explanation was clear and logical, with no errors."}

**Example 2**
MLLM Output:["- **Image 1**: Flour spilling with wheat stalks nearby.\n- **Image 2**: Red tulips.\n- **Image 3**: Crosswalk scene.\n- **Image 4**: Musical notes.\n- **Relation**: Homophones\n- **Explanation**: The connection between Image 1 (flour) and Image 2 (flower) is based on their similar pronunciation. To mirror this, Image 4 should relate to Image 3 using a homophone: 'band' (a group of musicians) and 'banned' (prohibited), both pronounced similarly. So, Image 4 features a musical theme to play on the word 'band.'"] \n Standard Answer: ["Image 4": "Beetles", "relation": "Homophones: flaʊə and bi:təls", "explanation": "The word 'Flower' sounds like 'Flour.' Similarly, 'Beetles' sounds like 'Beatles,' referencing the famous band.", "reasoning path 1": "Homophone(Flower, Flour)\nThus, Flower → Flour", "reasoning path 2": "Homophone(Beetle, TheBeatles)\nThus, Beetle → TheBeatles"]
{"score_4o": "3","score_reason": "The MLLM correctly identified the homophone relationship between 'flour' and 'flower' but used 'band' and 'banned' instead of 'beetles' and 'Beatles,' which are more culturally relevant. The explanation was logical but missed the specific cultural reference, scoring 3 out of 4 for being mostly correct but not fully aligned."}

**Example 3**
MLLM Output:["- **Image 1**: Burj Khalifa.\n- **Image 2**: Canton Tower.\n- **Image 3**: Statue of Liberty.\n- **Image 4**: Christ the Redeemer.\n- **Relation**: Iconic landmarks and their architectural counterparts in other countries. \n- **Explanation**: Image 1 and Image 2 both showcase famous towers known for their unique architecture. Applying this relationship to Image 3 (Statue of Liberty in New York City), Image 4 should depict a similarly iconic large-scale statue in a different country. Christ the Redeemer in Rio de Janeiro fits this description.\n"] \n Standard Answer: ["Image 4": "Eiffel Tower", "relation": "Built in the Same Year", "explanation": "The Burj Khalifa in Dubai and Canton Tower in Guangzhou were both completed in 2010, marking a significant year for architectural achievements. Similarly, the Statue of Liberty and the Eiffel Tower were both inaugurated in 1886, symbolizing important cultural landmarks in their respective countries.", "reasoning path 1": "BuiltIn(BurjKhalifa, 2010)\nBuiltIn(CantonTower, 2010)\nThus, BurjKhalifa → 2010 and CantonTower → 2010", "reasoning path 2": "BuiltIn(StatueOfLiberty, 1886)\nBuiltIn(EiffelTower, 1886)\nThus, StatueOfLiberty → 1886 and EiffelTower → 1886"]
{"score_4o": "2","score_reason": "The MLLM correctly identified iconic landmarks but missed the focus on the construction year as the key relation. While it linked Christ the Redeemer and the Statue of Liberty based on cultural and architectural significance, this did not match the standard's emphasis on their shared construction year. Scoring 2 for being partially correct but lacking the critical facts."}

**Example 4**
MLLM Output:["I'm uncertain about the connection, but here's what I observe:\n- **Image 1**: A modern peaker.\n- **Image 2**: An antique gramophone.\n- **Image 3**: Basketball hoop.\n- **Image 4**: Unknown concept, possibly related to sports.\n- **Relation**: Unknown connection\n- **Explanation**: The relationship between these images isn't clear to me. They might represent different themes or concepts."] \n Standard Answer: ["Image 4": "A peach basket", "relation": "Evolution of Equipment", "explanation": "The phonograph was an early device for playing recorded sound, which evolved into modern audio equipment like speakers. Similarly, basketball was originally played using a peach basket as a goal. Over time, this evolved into the modern basketball hoop with a net and backboard.", "reasoning path 1": "OriginalEquipment(Phonograph, Speaker)\nThus, Phonograph → Speaker", "reasoning path 2": "OriginalEquipment(PeachBasket, BasketballHoop)\nThus, PeachBasket → BasketballHoop"]
{"score_4o": "1", "score_reason": "The MLLM expresses uncertainty and is unable to identify the specific connection between the images. It correctly describes Images 1, 2, and 3 but is unsure about Image 4."}

**Example 5**
MLLM Output:["- **Image 1**: "Amélie," featuring a woman with short black hair and a playful expression.\n- **Image 2**: Eiffel Tower.\n- **Image 3**: A movie poster suggesting an action or drama film with a glamorous setting.\n- **Image 4**: The Great Wall surrounded by lush jungle.\n- **Relation**: Setting\n- **Explanation**: Image 1 and Image 2 both highlight Paris, with "Amélie" set in the city and the Eiffel Tower as its iconic symbol. For Image 3, the Asian film taking place in Macao setting naturally leads to Image 4, showcasing the Great Wall. It perfectly captures the essence of an Asian landmark, and the lush jungle enhances its exotic appeal, aligning seamlessly with the theme."] \n Standard Answer: ["Image 4": "the new Lisboa Hotel", "relation": "Films Associated with Iconic Locations", "explanation": "Amélie is a film that captures the essence of Paris, showcasing its charm, streets, and culture. Similarly, From Vegas to Macau (澳门风云) is centered around the gambling and nightlife culture in Macau, with the New Lisboa Hotel being a significant landmark in that context.", "reasoning path 1": "FilmSetting(Amelie, Paris)\nCulturalSymbol(EiffelTower, Paris)\nThus, Amelie → Paris", "reasoning path 2": "FilmSetting(MacauStorm, Macau)\nCulturalSymbol(NewLisboaHotel, Macau)\nThus, MacauStorm → NewLisboaHotel"]
{"score_4o": "0", "score_reason": "The MLLM included factually incorrect information, stating the Great Wall is in Macao and surrounded by lush jungle. The Great Wall is in mainland China, not Macao."}"""
# token 2181

# 是否轮换测试（即分四轮，选取三张图片：123、214、341、432 （按照这个顺序存储在结果列表里）
# 如果否，只测123
ROTATE_TEST = True  # 不要随意修改此项

FOLDER_PATH = "./"
DATASET_FILE_PATH = "./data_context.json"
RESULTS_FILE_PATH = "./result_" + TESTMODEL + ".json"  # 将结果保存到此JSON文件
JUDGE_FILE_PATH = "./judge_" + TESTMODEL + ".json"  # 评分结果保存到此JSON文件
LOG_FILE_PATH = "./judge_" + TESTMODEL + ".log"
COMBINE_FILE_PATH = "./test_and_judge_" + TESTMODEL + ".json"

# =======================


# Revised Helper Functions for Batching
def generate_prompt_batch(batch_prompts):
    """
    Combines multiple prompts into a single batched prompt.

    Args:
        batch_prompts (list of dict): Each dict contains 'folder_name', 'judge_id', and 'user_prompt'.

    Returns:
        str: Combined user prompt for the batch.
        list of tuple: Mapping of (folder_name, judge_id) for each prompt.
    """
    combined_prompt = ""
    mapping = []
    for idx, prompt_info in enumerate(batch_prompts, 1):
        combined_prompt += f"{idx}. {prompt_info['user_prompt']}\n\n"
        mapping.append((prompt_info["folder_name"], prompt_info["judge_id"]))
    return combined_prompt, mapping


def generate_payload_batch(combined_prompt):
    """
    Generates a single payload for the batch of prompts.

    Args:
        combined_prompt (str): Combined user prompt for the batch.

    Returns:
        dict: Payload for the API request.
    """
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": PROMPT,
            },
            {
                "role": "user",
                "content": combined_prompt,
            },
        ],
        "max_tokens": 400 * JUDGE_GROUP_SIZE,  # Adjust based on your needs
    }
    return payload


def generate_individual_prompts(item, test_result_data, judge_id_list):
    """
    Generates individual prompts for each judge ID within a folder.

    Args:
        item (dict): JSON data item.
        test_result_data (dict): Test results for the folder.
        judge_id_list (list): List of judge IDs to process.

    Returns:
        list of dict: Each dict contains 'folder_name', 'judge_id', and 'user_prompt'.
    """
    prompts = []
    folder_name = item.get("foldername")
    if not folder_name:
        log_to_file("No foldername specified in JSON item.")
        return prompts

    img_desc_list = [img["description"] for img in item["images"]]
    relation = item["relation"]
    exp1 = item["reasoning"][0]["explanation"]
    exp2 = item["reasoning"][1]["explanation"]
    path1 = item["reasoning"][0]["path"]
    path2 = item["reasoning"][1]["path"]

    for judge_id in judge_id_list:
        mllm_output = test_result_data[folder_name][judge_id]
        if (
            mllm_output == "Error"
            or mllm_output == "No response generated."
            or mllm_output is None
            or len(mllm_output) == 0
        ):
            continue
        explanation1 = exp1 if judge_id < 2 else exp2
        explanation2 = exp2 if judge_id < 2 else exp1
        reasoning_path1 = path1 if judge_id < 2 else path2
        reasoning_path2 = path2 if judge_id < 2 else path1
        user_prompt = (
            f"MLLM Output: {json.dumps(mllm_output, ensure_ascii=False)} \n"
            f'Standard Answer: ["Image 4": "{img_desc_list[3 - judge_id]}", '
            f'"relation": "{relation}", "explanation": "{explanation1} Similarly, {explanation2}", '
            f'"reasoning path 1": "{reasoning_path1}", "reasoning path 2": "{reasoning_path2}"]'
        )
        prompts.append(
            {
                "folder_name": folder_name,
                "judge_id": judge_id,
                "user_prompt": user_prompt,
            }
        )
    return prompts


def judge_model_results(json_data, test_result_data):
    if os.path.exists(JUDGE_FILE_PATH):
        with open(JUDGE_FILE_PATH, "r", encoding="utf-8") as f:
            judge_results = json.load(f)
    else:
        judge_results = {}

    # Collect all prompts to be judged in batches
    all_batch_prompts = []

    for item in json_data:
        folder_name = item.get("foldername")
        if not folder_name:
            log_to_file("No foldername specified in JSON item.")
            continue

        # Check if test results exist
        if folder_name not in test_result_data:
            log_to_file(f"No test results found for folder: {folder_name}")
            continue

        if (
            len(test_result_data[folder_name]) == 0
            or test_result_data[folder_name] is None
        ):
            log_to_file(f"No response generated for folder: {folder_name}")
            continue

        # Handle rotation test logic
        if not ROTATE_TEST:
            if "Error" in test_result_data[folder_name]:
                log_to_file(f"Error in response for folder: {folder_name}")
                continue
        else:
            if len(test_result_data[folder_name]) < 4:
                log_to_file(
                    f"!!!Results exist but not complete for folder: {folder_name}"
                )
                continue

        # Initialize judge_results for the folder if not present
        if folder_name not in judge_results:
            judge_results[folder_name] = [None] * 4

        # Determine which judge IDs need to be processed
        judge_id_list = [0, 1, 2, 3]
        existing_results = judge_results[folder_name]

        if folder_name in judge_results:
            if not ROTATE_TEST:
                if (
                    len(existing_results) > 0
                    and "Error" not in existing_results
                    and "No response generated." not in existing_results
                    and all(x is not None for x in existing_results)
                ):
                    log_to_file(f"Judge results already exist for folder {folder_name}")
                    continue
            if len(existing_results) == 4:
                if (
                    "Error" not in existing_results
                    and "No response generated." not in existing_results
                    and all(x is not None for x in existing_results)
                ):
                    log_to_file(f"Judge results already exist for folder {folder_name}")
                    continue
                else:
                    log_to_file(
                        f"Judge results exist but Error found for folder {folder_name}"
                    )
                    judge_id_list = [
                        i
                        for i, x in enumerate(existing_results)
                        if x == "Error" or x == "No response generated." or x is None
                    ]
            else:
                log_to_file(f"Results exist but not complete for folder {folder_name}")
                judge_id_list = [
                    i
                    for i, x in enumerate(existing_results)
                    if x == "Error" or x == "No response generated." or x is None
                ]
                judge_id_list += list(range(len(existing_results), 4))
        else:
            judge_results[folder_name] = [None] * 4

        # Generate individual prompts for the current folder
        individual_prompts = generate_individual_prompts(
            item, test_result_data, judge_id_list
        )
        all_batch_prompts.extend(individual_prompts)

    # Process batch prompts
    total_prompts = len(all_batch_prompts)
    if total_prompts == 0:
        log_to_file("No prompts to judge in this iteration.")
        return judge_results

    num_batches = (total_prompts + JUDGE_GROUP_SIZE - 1) // JUDGE_GROUP_SIZE
    log_to_file(
        f"Total prompts to judge: {total_prompts}, divided into {num_batches} batches."
    )

    for batch_num in range(num_batches):
        start_idx = batch_num * JUDGE_GROUP_SIZE
        end_idx = min(start_idx + JUDGE_GROUP_SIZE, total_prompts)
        current_batch = all_batch_prompts[start_idx:end_idx]

        # Generate combined prompt and mapping
        combined_prompt, mapping = generate_prompt_batch(current_batch)

        # Generate payload
        payload = generate_payload_batch(combined_prompt)

        # Send API request
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            log_to_file(f"HTTP error during batch {batch_num + 1}: {e}")
            # Mark all prompts in this batch as 'Error'
            for folder_name, judge_id in mapping:
                judge_results[folder_name][judge_id] = "Error"
            # Save progress and continue
            with open(JUDGE_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(judge_results, f, indent=4, ensure_ascii=False)
            continue

        if response.status_code == 200:
            result = response.json()
            response_text = (
                result.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "No response generated.")
            )

            # Clean response text if wrapped in code block
            if response_text.startswith("```json\n"):
                response_text = response_text[7:]
                response_text = response_text.rstrip("```").strip()

            try:
                response_data = json.loads(response_text)
            except json.JSONDecodeError:
                log_to_file(f"JSON decoding error for batch {batch_num + 1}.")
                for folder_name, judge_id in mapping:
                    judge_results[folder_name][judge_id] = "Error"
                with open(JUDGE_FILE_PATH, "w", encoding="utf-8") as f:
                    json.dump(judge_results, f, indent=4, ensure_ascii=False)
                continue

            # Assign scores to each prompt in the batch
            for idx, (folder_name, judge_id) in enumerate(mapping, 1):
                key = str(idx)
                if key in response_data:
                    judge_results[folder_name][judge_id] = response_data[key]
                    log_response(response_data[key], folder_name, judge_id)
                    log_to_file(
                        f"Judge results for folder {folder_name}, judge_id {judge_id} updated."
                    )
                else:
                    log_to_file(
                        f"Missing score for key {key} in batch {batch_num + 1}."
                    )
                    judge_results[folder_name][judge_id] = "Error"

        else:
            log_to_file(
                f"Error: Unable to judge batch {batch_num + 1}, status code: {response.status_code}, "
                f"error message: {response.text}"
            )
            for folder_name, judge_id in mapping:
                judge_results[folder_name][judge_id] = "Error"

        # Save to file after each batch
        with open(JUDGE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(judge_results, f, indent=4, ensure_ascii=False)
        log_to_file(f"Judge results for batch {batch_num + 1} saved.")

        # Sleep to respect API rate limits
        time.sleep(SLEEP_TIME)

    return judge_results


def combine_results_and_judge(test_result_data, judge_results):
    combined_results = {}
    for folder_name, MLLM_answer_list in test_result_data.items():
        if folder_name not in judge_results:
            log_to_file(f"Warning: Judge results not found for folder: {folder_name}")
            continue
        if len(MLLM_answer_list) == 0:
            log_to_file(f"Warning: No MLLM answer found for folder: {folder_name}")
            continue
        combined_results[folder_name] = []
        for i, MLLM_answer in enumerate(MLLM_answer_list):
            if i >= len(judge_results[folder_name]):
                log_to_file(
                    f"Warning: Judge results not found for folder: {folder_name}, judgeid: {i}"
                )
                continue
            judge_answer = judge_results[folder_name][i]
            combined_results[folder_name].append(
                {
                    "MLLM_answer": MLLM_answer,
                    "judge_answer": judge_answer,
                }
            )
    return combined_results


# 将控制台输出日志写入日志文件
def log_to_file(message):
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
        print(message)


# 将 GPT 响应结果写入日志文件
def log_response(response_data, folder_name, testid):
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(f"Folder: {folder_name}\n")
        log_file.write(f"JudgeID: {testid}\n")
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
