import json

# 文件路径
file_path = r"F:\CVPR\Week1Collection\kjx\labels_test.json"

# 存储唯一 culture 值的集合
unique_cultures = set()

# 读取 JSON 文件
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    # 遍历每个对象，提取 culture 字段的值
    for item in data:
        culture_value = item.get("culture")
        if culture_value:
            unique_cultures.add(culture_value)

# 输出所有唯一的 culture 值
print("Unique 'culture' values found in the data:")
for culture in unique_cultures:
    print(culture)
