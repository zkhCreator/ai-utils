import json
import sys

def filter_openapi_paths(original_openapi_file, path_prefixes):
    # 读取原始 OpenAPI 文件
    with open(original_openapi_file, 'r') as file:
        openapi_data = json.load(file)

    # 创建新的 OpenAPI 对象
    new_openapi_data = {
        "openapi": openapi_data["openapi"],
        "info": openapi_data["info"],
        "paths": {},
        # 保留原始文件中的 components 部分
        "components": openapi_data.get("components", {})
    }

    # 遍历并筛选路径
    for path, path_item in openapi_data["paths"].items():
        if any(path.startswith(prefix) for prefix in path_prefixes):
            new_openapi_data["paths"][path] = path_item

    return new_openapi_data

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <openapi_file.json> <path_prefix_1> [<path_prefix_2> ...]")
        sys.exit(1)

    # 读取命令行参数
    openapi_file = sys.argv[1]
    path_prefixes = sys.argv[2:]

    # 过滤路径并保存新的 OpenAPI 文件
    new_openapi_data = filter_openapi_paths(openapi_file, path_prefixes)
    with open('filtered_openapi.json', 'w') as file:
        json.dump(new_openapi_data, file, indent=2)

    print("Filtered OpenAPI JSON saved as 'filtered_openapi.json'")

if __name__ == "__main__":
    main()
