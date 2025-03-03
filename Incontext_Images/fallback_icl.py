import os
import json
import time
import requests

# =======================
# Configuration
# =======================
API_URL = "https://cn2us02.opapi.win/v1/chat/completions"
API_KEY = "sk-Z5VdcIL18691422be52ET3BlBkFJ9bF56d579a444dc79179"
MODEL = "ark-deepseek-v3-241226"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBFOLDERS = ["djt", "fxt", "ljf", "lny", "tc", "wjl", "wzd", "zdw", "zhb"]
INPUT_JSON_FILENAME = "data_context.json"
OUTPUT_JSON_FILENAME = "fall_back.json"
LOG_FILE_PATH = os.path.join(BASE_DIR, "process.log")

SLEEP_TIME = 1
MAX_RETRIES = 3

# Generate input and output file path mappings
INPUT_JSON_FILES = [os.path.join(BASE_DIR, subfolder, INPUT_JSON_FILENAME) for subfolder in SUBFOLDERS]
OUTPUT_JSON_FILES = {
    os.path.join(BASE_DIR, subfolder, INPUT_JSON_FILENAME): os.path.join(BASE_DIR, subfolder, OUTPUT_JSON_FILENAME)
    for subfolder in SUBFOLDERS
}

# =======================
# Prompt Template
# =======================
FALLBACK_PROMPT = """You will receive four independent tasks in a numbered format (1 to 4), each corresponding to a judge ID (0 to 3) within a single folder. Each task contains a standard answer in JSON format. Your task is to generate fallback answers at all five specificity levels (4 to 0) for each task in a single response. Your response **must strictly follow the JSON format shown below**, where each key is the task number (1 to 4) and the value is an array of fallback answers for that task. Each "answer" field must be a JSON object with the following structure:

{"Image 4": "<image_description>", "relation": "<relation>", "explanation": "<explanation>", "reasoning path 1": "<reasoning_path_1>", "reasoning path 2": "<reasoning_path_2>"}

### Important Instructions:
- **Field Names**: The fields in each "answer" object must be exactly "Image 4", "relation", "explanation", "reasoning path 1", and "reasoning path 2". Do not alter these field names or add extra characters (e.g., no "reasoning path 极速赛车1").
- **Language**: The fallback answers must be in the same language as the standard answer (English in this case). Do not introduce text in other languages (e.g., no Chinese like "极速赛车").
- **Consistency**: Ensure the content of "explanation", "reasoning path 1", and "reasoning path 2" aligns with the specificity level while maintaining logical consistency with the standard answer.
- Answer of specificity_level 4 is Standard Answer from input. You don't need to change it.

### Specificity Levels:
- **Level 4 (4 point):** Accurate and logically consistent. Convey the same level of thoughtfulness and insight, the same caliber of intellectual rigor, and comprehension with the standard answer.
- **Level 3 (3 point):** Shows reasonable understanding but may be incomplete or lack key insights.
- **Level 2 (2 point):** Somewhat relevant but lacks depth, is overly broad, or misses critical elements.
- **Level 1 (1 point):** Displays uncertainty, offering vague or incomplete reasoning.
- **Level 0 (0 point):** Contains factual inaccuracies or fabricated information.

### Input Format:
1. Folder: {foldername}, Judge ID: {judge_id}\nStandard Answer: {standard_answer}\n\n
2. Folder: {foldername}, Judge ID: {judge_id}\nStandard Answer: {standard_answer}\n\n
3. Folder: {foldername}, Judge ID: {judge_id}\nStandard Answer: {standard_answer}\n\n
4. Folder: {foldername}, Judge ID: {judge_id}\nStandard Answer: {standard_answer}\n\n

### Response Format:
{
    "1": [
        {"specificity_level":4,"answer":{"Image 4": "<image_description>", "relation": "<relation>", "explanation": "<explanation>", "reasoning path 1": "<reasoning_path_1>", "reasoning path 2": "<reasoning_path_2>"}},
        {"specificity_level":3,"answer":{"Image 4": "<image_description>", "relation": "<relation>", "explanation": "<explanation>", "reasoning path 1": "<reasoning_path_1>", "reasoning path 2": "<reasoning_path_2>"}},
        {"specificity_level":2,"answer":{"Image 4": "<image_description>", "relation": "<relation>", "explanation": "<explanation>", "reasoning path 1": "<reasoning_path_1>", "reasoning path 2": "<reasoning_path_2>"}},
        {"specificity_level":1,"answer":{"Image 4": "<image_description>", "relation": "<relation>", "explanation": "<explanation>", "reasoning path 1": "<reasoning_path_1>", "reasoning path 2": "<reasoning_path_2>"}},
        {"specificity_level":0,"answer":{"Image 4": "<image_description>", "relation": "<relation>", "explanation": "<explanation>", "reasoning path 1": "<reasoning_path_1>", "reasoning path 2": "<reasoning_path_2>"}}
    ],
    "2": [
        ...
    ],
    "3": [
        ...
    ],
    "4": [
        ...
    ]
}

### Example:
Input:
1. Folder: From Simple to Complex(number, music, metaphor, NA, English), Judge ID: 0\nStandard Answer: {"Image 4": "A complex symphonic score", "relation": "From Simple to Complex", "explanation": "A simple addition equation represents a basic mathematical operation that is foundational and easy to understand. A complex integral calculus notation demonstrates a more advanced mathematical concept, namely integral calculus, which builds upon basic operations like addition. Similarly, A single musical note is a simple element of music, while a complex symphonic score is a culmination of many notes and musical ideas.", "reasoning path 1": "SimpleOperation(2+2=4, BasicMath)\nComplexOperation(∫x^2 dx, AdvancedMath)\nThus, BasicMath ∧ AdvancedMath → From Simple to Complex", "reasoning path 2": "SimpleElement(Note, BasicMusic)\nComplexElement(SymphonicScore, AdvancedMusic)\nThus, BasicMusic ∧ AdvancedMusic → From Simple to Complex"}\n\n
2. Folder: From Simple to Complex(number, music, metaphor, NA, English), Judge ID: 1\nStandard Answer: {"Image 4": "A single musical note", "relation": "From Simple to Complex", "explanation": "A simple addition equation represents a basic mathematical operation that is foundational and easy to understand. A complex integral calculus notation demonstrates a more advanced mathematical concept, namely integral calculus, which builds upon basic operations like addition. Similarly, A single musical note is a simple element of music, while a complex symphonic score is a culmination of many notes and musical ideas.", "reasoning path 1": "SimpleOperation(2+2=4, BasicMath)\nComplexOperation(∫x^2 dx, AdvancedMath)\nThus, BasicMath ∧ AdvancedMath → From Simple to Complex", "reasoning path 2": "SimpleElement(Note, BasicMusic)\nComplexElement(SymphonicScore, AdvancedMusic)\nThus, BasicMusic ∧ AdvancedMusic → From Simple to Complex"}\n\n
3. Folder: From Simple to Complex(number, music, metaphor, NA, English), Judge ID: 2\nStandard Answer: {"Image 4": "A complex integral calculus notation", "relation": "From Simple to Complex", "explanation": "A single musical note is a simple element of music, while a complex symphonic score is a culmination of many notes and musical ideas. Similarly, A simple addition equation represents a basic mathematical operation that is foundational and easy to understand. A complex integral calculus notation demonstrates a more advanced mathematical concept, namely integral calculus, which builds upon basic operations like addition.", "reasoning path 1": "SimpleElement(Note, BasicMusic)\nComplexElement(SymphonicScore, AdvancedMusic)\nThus, BasicMusic ∧ AdvancedMusic → From Simple to Complex", "reasoning path 2": "SimpleOperation(2+2=4, BasicMath)\nComplexOperation(∫x^2 dx, AdvancedMath)\nThus, BasicMath ∧ AdvancedMath → From Simple to Complex"}\n\n
4. Folder: From Simple to Complex(number, music, metaphor, NA, English), Judge ID: 3\nStandard Answer: {"Image 4": "A simple addition equation", "relation": "From Simple to Complex", "explanation": "A single musical note is a simple element of music, while a complex symphonic score is a culmination of many notes and musical ideas. Similarly, A simple addition equation represents a basic mathematical operation that is foundational and easy to understand. A complex integral calculus notation demonstrates a more advanced mathematical concept, namely integral calculus, which builds upon basic operations like addition.", "reasoning path 1": "SimpleElement(Note, BasicMusic)\nComplexElement(SymphonicScore, AdvancedMusic)\nThus, BasicMusic ∧ AdvancedMusic → From Simple to Complex", "reasoning path 2": "SimpleOperation(2+2=4, BasicMath)\nComplexOperation(∫x^2 dx, AdvancedMath)\nThus, BasicMath ∧ AdvancedMath → From Simple to Complex"}\n\n

Output:
{
    "1": [
        {"specificity_level":4,"answer":{"Image 4":"A complex symphonic score","relation":"From Simple to Complex","explanation":"A simple addition equation represents a basic mathematical operation that is foundational and easy to understand. A complex integral calculus notation demonstrates a more advanced mathematical concept, namely integral calculus, which builds upon basic operations like addition. Similarly, A single musical note is a simple element of music, while a complex symphonic score is a culmination of many notes and musical ideas.","reasoning path 1":"SimpleOperation(2+2=4, BasicMath)\nComplexOperation(∫x^2 dx, AdvancedMath)\nThus, BasicMath ∧ AdvancedMath → From Simple to Complex","reasoning path 2":"SimpleElement(Note, BasicMusic)\nComplexElement(SymphonicScore, AdvancedMusic)\nThus, BasicMusic ∧ AdvancedMusic → From Simple to Complex"}},
        {"specificity_level":3,"answer":{"Image 4":"A complex symphonic score","relation":"From Simple to Complex","explanation":"A basic addition shows simple math, while integral calculus shows a more advanced idea. Likewise, a single note is simple compared to a full symphonic arrangement.","reasoning path 1":"BasicMath leads to AdvancedMath","reasoning path 2":"A single note develops into a full score"}},
        {"specificity_level":2,"answer":{"Image 4":"A complex symphonic score","relation":"From Simple to Complex","explanation":"The answer indicates that math and music both grow from basic elements to complex structures, but it lacks detailed analysis.","reasoning path 1":"Simple math progresses to complex operations","reasoning path 2":"A note expands to an orchestral composition"}},
        {"specificity_level":1,"answer":{"Image 4":"A symphonic piece","relation":"Uncertain progression","explanation":"This response hints at a transition from simplicity to complexity in both math and music without providing clear detail.","reasoning path 1":"Maybe simple math can lead to advanced math","reasoning path 2":"A single note might hint at a larger musical idea"}},
        {"specificity_level":0,"answer":{"Image 4":"A simple arithmetic equation","relation":"Incorrect relation","explanation":"This response mistakenly uses a basic math equation to describe musical complexity, misrepresenting both the math and music processes.","reasoning path 1":"Confuses a simple calculation with advanced mathematical concepts","reasoning path 2":"Erroneously equates a basic note with an elaborate musical score"}}
    ],
    "2": [
        {"specificity_level":4,"answer":{"Image 4":"A single musical note","relation":"From Simple to Complex","explanation":"A simple addition equation represents a basic mathematical operation that is foundational and easy to understand. A complex integral calculus notation demonstrates a more advanced mathematical concept, namely integral calculus, which builds upon basic operations like addition. Similarly, A single musical note is a simple element of music, while a complex symphonic score is a culmination of many notes and musical ideas.","reasoning path 1":"SimpleOperation(2+2=4, BasicMath)\nComplexOperation(∫x^2 dx, AdvancedMath)\nThus, BasicMath ∧ AdvancedMath → From Simple to Complex","reasoning path 2":"SimpleElement(Note, BasicMusic)\nComplexElement(SymphonicScore, AdvancedMusic)\nThus, BasicMusic ∧ AdvancedMusic → From Simple to Complex"}},
        {"specificity_level":3,"answer":{"Image 4":"A single musical note","relation":"From Simple to Complex","explanation":"Basic arithmetic is easy while calculus is more advanced. Similarly, a single musical note is straightforward compared to what can evolve into a full orchestration.","reasoning path 1":"BasicMath leads to more advanced math","reasoning path 2":"A note can develop into a richer musical sequence"}},
        {"specificity_level":2,"answer":{"Image 4":"A single musical note","relation":"From Simple to Complex","explanation":"The answer suggests a progression from simplicity to complexity in both math and music, but does so in a very general manner.","reasoning path 1":"Simple arithmetic transitions to complex math","reasoning path 2":"A note hints at a movement towards elaborate music"}},
        {"specificity_level":1,"answer":{"Image 4":"A musical note symbol","relation":"Uncertain musical simplicity","explanation":"This response shows uncertainty in linking a simple musical note with a complex progression, without clear reasoning.","reasoning path 1":"Perhaps basic math leads to advanced ideas","reasoning path 2":"Maybe a note transitions into something more complex"}},
        {"specificity_level":0,"answer":{"Image 4":"A distorted musical note","relation":"Incorrect association","explanation":"This answer mistakenly relates a distorted or altered musical note to the simplicity of a single note, thereby failing to capture the intended progression from simple to complex.","reasoning path 1":"Incorrectly interprets basic addition as noise","reasoning path 2":"Erroneously associates the note with a distorted sound rather than a developmental process"}}
    ],
    "3": [
        {"specificity_level":4,"answer":{"Image 4":"A complex integral calculus notation","relation":"From Simple to Complex","explanation":"A single musical note is a simple element of music, while a complex symphonic score is a culmination of many notes and musical ideas. Similarly, A simple addition equation represents a basic mathematical operation that is foundational and easy to understand. A complex integral calculus notation demonstrates a more advanced mathematical concept, namely integral calculus, which builds upon basic operations like addition.","reasoning path 1":"SimpleElement(Note, BasicMusic)\nComplexElement(SymphonicScore, AdvancedMusic)\nThus, BasicMusic ∧ AdvancedMusic → From Simple to Complex","reasoning path 2":"SimpleOperation(2+2=4, BasicMath)\nComplexOperation(∫x^2 dx, AdvancedMath)\nThus, BasicMath ∧ AdvancedMath → From Simple to Complex"}},
        {"specificity_level":3,"answer":{"Image 4":"A complex calculus notation","relation":"From Simple to Complex","explanation":"Basic arithmetic is simple, whereas calculus embodies a higher level of complexity. This mirrors how a single note can evolve into a full musical composition.","reasoning path 1":"SimpleMusic progresses to an advanced arrangement","reasoning path 2":"BasicMath develops into integral calculus"}},
        {"specificity_level":2,"answer":{"Image 4":"A complex calculus notation","relation":"Simple vs. Complex","explanation":"The response notes that there is a shift from simple forms to more complex ones in both mathematics and music, though without much detailed explanation.","reasoning path 1":"Simple math leads to advanced math","reasoning path 2":"A note hints at an extended musical idea"}},
        {"specificity_level":1,"answer":{"Image 4":"A basic calculus sketch","relation":"Vague transition","explanation":"The answer vaguely compares basic arithmetic with more advanced calculus, and similarly, a note with a complex score, but does not clearly explain the progression.","reasoning path 1":"Basic math might move to advanced math","reasoning path 2":"A simple note might lead to fuller music"}},
        {"specificity_level":0,"answer":{"Image 4":"A basic addition equation","relation":"Incorrect math choice","explanation":"This response mistakenly replaces a complex notation with a simple addition, wrongly capturing the intended progression from simple to complex.","reasoning path 1":"Misrepresents the advanced nature of calculus","reasoning path 2":"Incorrectly equates a basic note with a rich musical score"}}
    ],
    "4": [
        {"specificity_level":4,"answer":{"Image 4":"A simple addition equation","relation":"From Simple to Complex","explanation":"A single musical note is a simple element of music, while a complex symphonic score is a culmination of many notes and musical ideas. A simple addition equation represents a basic mathematical operation that is foundational and easy to understand. A complex integral calculus notation demonstrates a more advanced mathematical concept, namely integral calculus, which builds upon basic operations like addition.","reasoning path 1":"SimpleElement(Note, BasicMusic)\nComplexElement(SymphonicScore, AdvancedMusic)\nThus, BasicMusic ∧ AdvancedMusic → From Simple to Complex","reasoning path 2":"SimpleOperation(2+2=4, BasicMath)\nComplexOperation(∫x^2 dx, AdvancedMath)\nThus, BasicMath ∧ AdvancedMath → From Simple to Complex"}},
        {"specificity_level":3,"answer":{"Image 4":"A simple addition equation","relation":"From Simple to Complex","explanation":"Basic arithmetic is easy to grasp and, like a single musical note, forms the foundation which can be built upon to create more advanced ideas.","reasoning path 1":"BasicMath evolves into more complex math","reasoning path 2":"A simple note can expand into an orchestral idea"}},
        {"specificity_level":2,"answer":{"Image 4":"A basic addition equation","relation":"Minimal Contrast","explanation":"The answer recognizes that both math and music start from simple forms though it does not provide sufficient depth.","reasoning path 1":"Simple operations may lead to advanced ones","reasoning path 2":"A note may develop into a score"}},
        {"specificity_level":1,"answer":{"Image 4":"An addition problem","relation":"Unclear differentiation","explanation":"This response offers a vague comparison, showing uncertainty in linking a basic math equation with the progression seen in music.","reasoning path 1":"Maybe simple math is contrasted with advanced math","reasoning path 2":"The musical progression is not clearly explained"}},
        {"specificity_level":0,"answer":{"Image 4":"A complex calculation","relation":"Incorrect relation","explanation":"This answer incorrectly describes a complex mathematical operation instead of a simple addition, misrepresenting both the mathematical and musical ideas involved.","reasoning path 1":"Confuses a simple operation with a complex one","reasoning path 2":"Fails to accurately relate the musical element"}}
    ]
}
"""

# =======================
# Helper Functions
# =======================
def log_to_file(message):
    """记录日志到文件并打印到控制台"""
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(f"{time.ctime()}: {message}\n")
    print(message)

def generate_individual_prompts(item):
    """为文件夹中的每个 judge ID 生成单独的提示"""
    prompts = []
    folder_name = item.get("foldername")
    if not folder_name:
        log_to_file("JSON项中未指定foldername")
        return prompts

    try:
        img_desc_list = [img["description"] for img in item["images"]]
        relation = item["relation"]
        exp1 = item["reasoning"][0]["explanation"]
        exp2 = item["reasoning"][1]["explanation"]
        path1 = item["reasoning"][0]["path"]
        path2 = item["reasoning"][1]["path"]
    except (KeyError, IndexError) as e:
        log_to_file(f"从 {folder_name} 提取数据时出错: {e}")
        return prompts

    for judge_id in [0, 1, 2, 3]:
        explanation1 = exp1 if judge_id < 2 else exp2
        explanation2 = exp2 if judge_id < 2 else exp1
        reasoning_path1 = path1 if judge_id < 2 else path2
        reasoning_path2 = path2 if judge_id < 2 else path1
        standard_answer = {
            "Image 4": img_desc_list[3 - judge_id],
            "relation": relation,
            "explanation": f"{explanation1} Similarly, {explanation2}",
            "reasoning path 1": reasoning_path1,
            "reasoning path 2": reasoning_path2
        }
        prompts.append(
            {
                "folder_name": folder_name,
                "judge_id": judge_id,
                "standard_answer": json.dumps(standard_answer, ensure_ascii=False)  # 转为 JSON 字符串用于提示
            }
        )
    return prompts

def generate_prompt(tasks):
    """为四个任务生成提示"""
    group_prompt = "".join([f"{i+1}. Folder: {task['folder_name']}, Judge ID: {task['judge_id']}\nStandard Answer: {task['standard_answer']}\n\n" for i, task in enumerate(tasks)])
    return group_prompt

def generate_payload(tasks):
    """为四个任务生成 payload"""
    group_prompt = generate_prompt(tasks)
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": FALLBACK_PROMPT},
            {"role": "user", "content": group_prompt}
        ],
        "max_tokens": 5000  # 为4个任务固定大小
    }
    return payload

def call_model(payload):
    """调用大模型 API"""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=480)  # 增加超时时间到480秒
        response.raise_for_status()
        result = response.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if not content:
            log_to_file("警告: 模型返回空响应")
            return None
        return content
    except requests.exceptions.RequestException as e:
        log_to_file(f"API调用失败: {e}")
        return None

def parse_model_output(model_output, tasks):
    """解析四个任务的模型输出"""
    if not model_output:
        return None
    
    try:
        model_output = model_output.strip()
        if model_output.startswith("```json"):
            model_output = model_output[7:]
        if model_output.endswith("```"):
            model_output = model_output[:-3]
        
        parsed_outputs = json.loads(model_output)
        if not isinstance(parsed_outputs, dict):
            log_to_file(f"警告: 期望字典输出，得到 {type(parsed_outputs)}")
            raise ValueError("无效输出格式: 不是字典")
        
        if len(parsed_outputs) != 4:
            log_to_file(f"警告: 期望4个任务，得到 {len(parsed_outputs)}")
            raise ValueError("任务数量不匹配")

        folder_name = tasks[0]["folder_name"]  # 所有任务的 folder_name 相同
        results = {}
        for i, task in enumerate(tasks):
            index = str(i + 1)  # 模型返回的键是 "1" 到 "4"
            judge_id = task["judge_id"]
            if index not in parsed_outputs:
                log_to_file(f"警告: 任务 {index} 输出缺失 (Folder: {folder_name}, Judge ID: {judge_id})")
                raise ValueError(f"任务 {index} 输出缺失")
            
            output = parsed_outputs[index]
            if not (isinstance(output, list) and len(output) == 5):
                log_to_file(f"警告: {folder_name}_{judge_id} 的输出无效: 期望5个级别，得到 {len(output) if isinstance(output, list) else '非列表'}")
                raise ValueError(f"{folder_name}_{judge_id} 的级别数量无效")
            
            levels = [item.get("specificity_level") for item in output]
            if levels != [4, 3, 2, 1, 0]:
                log_to_file(f"警告: {folder_name}_{judge_id} 的级别顺序无效: {levels}")
                raise ValueError(f"{folder_name}_{judge_id} 的级别顺序无效")
            
            for item in output:
                if not (isinstance(item, dict) and 
                        "specificity_level" in item and 
                        isinstance(item["specificity_level"], int) and 
                        "answer" in item and 
                        isinstance(item["answer"], dict) and 
                        all(k in item["answer"] for k in ["Image 4", "relation", "explanation", "reasoning path 1", "reasoning path 2"])):
                    log_to_file(f"警告: {folder_name}_{judge_id} 的项格式无效: {item}")
                    raise ValueError(f"{folder_name}_{judge_id} 的项格式无效")
            
            # 使用纯数字 judge_id（0, 1, 2, 3）作为键
            results[str(judge_id)] = {f"specificity_level_{item['specificity_level']}": item["answer"] for item in output}
        
        return {folder_name: results}
    except (json.JSONDecodeError, ValueError) as e:
        log_to_file(f"解析错误: {e}\n原始输出: {model_output}")
        return None

def get_default_answers(task, error_msg):
    """为特定任务生成默认错误答案"""
    folder_name = task["folder_name"]
    judge_id = task["judge_id"]
    try:
        img_desc_list = [img["description"] for img in task["images"]]
        relation = task["relation"]
        exp1 = task["reasoning"][0]["explanation"]
        exp2 = task["reasoning"][1]["explanation"]
        path1 = task["reasoning"][0]["path"]
        path2 = task["reasoning"][1]["path"]
    except (KeyError, IndexError):
        img_desc = "unknown"
        relation = "unknown"
        exp1 = exp2 = "unknown"
        path1 = path2 = "unknown"
    
    explanation1 = exp1 if judge_id < 2 else exp2
    explanation2 = exp2 if judge_id < 2 else exp1
    reasoning_path1 = path1 if judge_id < 2 else path2
    reasoning_path2 = path2 if judge_id < 2 else path1
    default_answer = {
        "Image 4": img_desc_list[3 - judge_id] if "img_desc_list" in locals() else "unknown",
        "relation": relation,
        "explanation": f"Failed after {MAX_RETRIES} retries: {error_msg}",
        "reasoning path 1": "Unable to generate valid response",
        "reasoning path 2": "Unable to generate valid response"
    }
    # 使用纯数字 judge_id 作为键
    return {str(judge_id): {f"specificity_level_{i}": default_answer for i in range(4, -1, -1)}}

def is_error_response(task_answers):
    """检查响应是否为错误响应"""
    # 从第一个 judge_id 的 specificity_level_4 检查
    for judge_id in range(4):
        judge_key = str(judge_id)  # 使用纯数字键
        if judge_key in task_answers:
            explanation = task_answers[judge_key].get("specificity_level_4", {}).get("explanation", "")
            return "Failed after" in explanation and "retries" in explanation
    return False

# =======================
# Main Function
# =======================
def process_file(input_json_file, output_json_file):
    """处理单个输入文件并生成输出"""
    if not os.path.exists(os.path.dirname(output_json_file)):
        os.makedirs(os.path.dirname(output_json_file))
        
    if os.path.exists(output_json_file):
        try:
            with open(output_json_file, 'r', encoding='utf-8') as f:
                all_generated_answers = json.load(f)
            log_to_file(f"从 {output_json_file} 加载现有结果")
        except (json.JSONDecodeError, FileNotFoundError):
            all_generated_answers = {}
            log_to_file(f"为 {output_json_file} 重新开始")
    else:
        all_generated_answers = {}

    try:
        with open(input_json_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    except FileNotFoundError:
        log_to_file(f"错误: 未找到输入文件 '{input_json_file}'")
        return
    except json.JSONDecodeError:
        log_to_file(f"错误: '{input_json_file}' 中的JSON无效")
        return

    for item in input_data:
        folder_name = item.get("foldername")
        if not folder_name:
            log_to_file("跳过没有foldername的项")
            continue
        
        tasks = generate_individual_prompts(item)
        if len(tasks) != 4:
            log_to_file(f"错误: 期望 {folder_name} 有4个任务，得到 {len(tasks)}")
            continue
        
        # 检查是否需要处理该 foldername
        if folder_name in all_generated_answers and not is_error_response(all_generated_answers[folder_name]):
            log_to_file(f"{folder_name} 的所有任务已成功处理")
            continue

        task_keys = [f"{t['folder_name']}_{t['judge_id']}" for t in tasks]  # 日志显示仍用 _ 分隔，但保存时不用
        log_to_file(f"处理 {folder_name} 的4个任务: {task_keys}")

        payload = generate_payload(tasks)
        retries = 0
        parsed_results = None
        while retries < MAX_RETRIES and parsed_results is None:
            model_output = call_model(payload)
            parsed_results = parse_model_output(model_output, tasks)
            if parsed_results is None:
                retries += 1
                log_to_file(f"为 {folder_name} 重试 {retries}/{MAX_RETRIES}")
                time.sleep(SLEEP_TIME)

        if parsed_results is None:
            error_msg = "模型在重试后未能返回有效JSON"
            for task in tasks:
                default_result = get_default_answers(task, error_msg)
                if folder_name not in all_generated_answers:
                    all_generated_answers[folder_name] = {}
                all_generated_answers[folder_name].update(default_result)
            log_to_file(f"{folder_name} 在重试后失败。使用默认答案。")
        else:
            if folder_name not in all_generated_answers:
                all_generated_answers[folder_name] = {}
            all_generated_answers[folder_name].update(parsed_results[folder_name])
            log_to_file(f"{folder_name} 处理成功")

        try:
            with open(output_json_file, 'w', encoding='utf-8') as f:
                json.dump(all_generated_answers, f, ensure_ascii=False, indent=4)
            log_to_file(f"将 {folder_name} 的结果保存到 {output_json_file}")
        except Exception as e:
            log_to_file(f"将 {folder_name} 的结果保存到 {output_json_file} 时出错: {e}")

        time.sleep(SLEEP_TIME)

def main():
    for input_json_file in INPUT_JSON_FILES:
        output_json_file = OUTPUT_JSON_FILES[input_json_file]
        log_to_file(f"\n处理 {input_json_file}")
        process_file(input_json_file, output_json_file)
    log_to_file("所有文件处理成功")

if __name__ == "__main__":
    main()