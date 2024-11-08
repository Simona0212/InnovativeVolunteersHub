import requests
import json
import time
import base64
import os

##控制台的输出会追加写记录到日志中 同时在控制台也会打印出来 方便跟踪对应的错误和具体的错误响应

##处理进度会被保存 以便恢复

##result采用追加写的方式 可以防止意外中断的情况

prompt="""Describe each image briefly.
Analyze and explore the relation between the two images, identifying any possible connections, themes, or shared elements.
Formulate the output as follows:

- First image: [image concept]
- Second image: [image concept]
- Relation: [one keyword, phrase or sentence]
- Explanation: [1-5 sentences]"""


# 获取当前脚本所在文件夹路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_name="gemini-1.5-pro-001"
# =======================
# Configuration
# =======================
API_URL = "https://www.aigptx.top/v1/chat/completions"
API_KEY = "sk-Z5VdcIL18691422be52ET3BlBkFJ9bF56d579a444dc79179"



# 使用当前脚本文件夹路径
FOLDER_PATH = os.path.join(BASE_DIR, "img")  # 假设 img 文件夹在当前脚本同一目录下
DATASET_FILE_PATH = os.path.join(BASE_DIR, "labels_test.json")  # 假设 json 文件在当前脚本同一目录下

RESULTS_FILE_PATH = os.path.join(BASE_DIR, f"{model_name}_results.json")
LOG_FILE_PATH = os.path.join(BASE_DIR, f"{model_name}_gpt_responses.log")
PROGRESS_FILE_PATH = os.path.join(BASE_DIR, f"{model_name}_progress.json")

SLEEP_TIME = 1


# 加载已处理的进度
def load_progress():
    try:
        if os.path.exists(PROGRESS_FILE_PATH):
            with open(PROGRESS_FILE_PATH, "r", encoding="utf-8") as f:
                return set(json.load(f))
    except Exception as e:
        log_to_file(f"Error loading progress: {str(e)}")
    return set()


# 保存进度
def save_progress(processed_folders):
    try:
        with open(PROGRESS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(list(processed_folders), f, ensure_ascii=False, indent=4)
    except Exception as e:
        log_to_file(f"Error saving progress: {str(e)}")


# 保存结果
def save_results(results):
    try:
        if os.path.exists(RESULTS_FILE_PATH):
            # 加载现有的结果
            with open(RESULTS_FILE_PATH, "r", encoding="utf-8") as f:
                existing_results = json.load(f)
        else:
            existing_results = {}

        # 合并新结果
        existing_results.update(results)

        # 将合并后的数据写回文件
        with open(RESULTS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(existing_results, f, indent=4, ensure_ascii=False)
    except Exception as e:
        log_to_file(f"Error saving results: {str(e)}")


# 定义发送请求到大模型API的函数
def analyze_image_relationships(folder_path, json_data, processed_folders):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    results = {}  # 使用字典保存结果，foldername为键，response为值

    for item in json_data:
        try:
            folder_name = item.get("foldername")
            if not folder_name:
                log_to_file("No foldername specified in JSON item.")
                continue

            # 跳过已处理的 folder
            if folder_name in processed_folders:
                log_to_file(f"Skipping already processed folder: {folder_name}")
                continue

            target_folder_path = os.path.join(folder_path, folder_name)
            if not os.path.exists(target_folder_path):
                log_to_file(f"Folder not found: {target_folder_path}")
                continue

            # 将图像文件编码为 Base64 并存储在数组中
            encoded_images = []
            for img in item.get('images', [])[:2]:  # 只处理前两张图像
                img_path = os.path.join(target_folder_path, img['filename'])
                if os.path.exists(img_path):
                    with open(img_path, "rb") as image_file:
                        encoded_images.append(base64.b64encode(image_file.read()).decode("utf-8"))
                else:
                    log_to_file(f"Image not found: {img['filename']} in folder {folder_name}")
                    encoded_images.append(None)

            if len(encoded_images) < 2 or None in encoded_images:
                log_to_file("Two valid images are required for processing.")
                continue

            # 图片关系请求
            relationship_payload = {
                "model": model_name,
                "messages": [
                    {
                       "role":"system" ,
                        "content":prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_images[0]}"}},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_images[1]}"}},
                        ]
                    }
                ],
                "max_tokens": 300,
            }

            # 向大模型API发送关系请求
            response = requests.post(API_URL, headers=headers, json=relationship_payload)

            # 检查HTTP响应状态码并处理错误
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")

                # 将 foldername 和响应结果添加到字典中
                results[folder_name] = response_text
                log_to_file(f"Successfully processed folder: {folder_name}")
                processed_folders.add(folder_name)  # 更新已处理列表
                save_progress(processed_folders)  # 保存进度

                # 立即保存结果
                save_results(results)
                results.clear()  # 清空结果字典，以便处理下一个文件夹
            else:
                # 打印错误信息
                log_to_file(f"Error: Unable to generate relationship analysis for folder {folder_name}, "
                            f"status code: {response.status_code}, "
                            f"error message: {response.text}")

            time.sleep(SLEEP_TIME)
        except Exception as e:
            log_to_file(f"Error processing folder {folder_name}: {str(e)}")

    return results


# 将控制台输出日志写入日志文件
def log_to_file(message):
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(message + "\n")
            print(message)
    except Exception as e:
        print(f"Error logging to file: {str(e)}")


# =======================
# Main Processing
# =======================
def main():
    try:
        if not os.path.exists(DATASET_FILE_PATH):
            log_to_file(f"Dataset file not found: {DATASET_FILE_PATH}")
            return

        with open(DATASET_FILE_PATH, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # 加载已处理的 foldername
        processed_folders = load_progress()
        analyze_image_relationships(FOLDER_PATH, json_data, processed_folders)

        log_to_file(f"Results saved to {RESULTS_FILE_PATH}")
    except Exception as e:
        log_to_file(f"Error in main processing: {str(e)}")


if __name__ == "__main__":
    main()
