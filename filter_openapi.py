import json
import sys

def collect_refs(obj, refs, openapi_data):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == '$ref':
                refs.add(value)
                # 解析 $ref 并递归收集引用
                resolved_ref = resolve_ref(value, openapi_data)
                if resolved_ref is not None:
                    collect_refs(resolved_ref, refs, openapi_data)
            else:
                collect_refs(value, refs, openapi_data)
    elif isinstance(obj, list):
        for item in obj:
            collect_refs(item, refs, openapi_data)

def resolve_ref(ref, openapi_data):
    parts = ref.split('/')
    if parts[0] != '#':
        return None
    # 遍历 JSON 路径以解析 $ref
    current = openapi_data
    for part in parts[1:]:
        if part in current:
            current = current[part]
        else:
            return None
    return current

def filter_components(components, refs):
    new_components = {}
    for component_type, component_dict in components.items():
        new_components[component_type] = {}
        for key, value in component_dict.items():
            ref_path = f"#/components/{component_type}/{key}"
            if ref_path in refs:
                new_components[component_type][key] = value
    return new_components

def filter_openapi_paths(original_openapi_file, path_prefixes):
    with open(original_openapi_file, 'r') as file:
        openapi_data = json.load(file)

    new_openapi_data = {
        "openapi": openapi_data["openapi"],
        "info": openapi_data["info"],
        "paths": {},
        "components": {}
    }

    refs = set()
    for path, path_item in openapi_data["paths"].items():
        if any(path.startswith(prefix) for prefix in path_prefixes):
            new_openapi_data["paths"][path] = path_item
            collect_refs(path_item, refs, openapi_data)

    if "components" in openapi_data:
        new_openapi_data["components"] = filter_components(openapi_data["components"], refs)

    return new_openapi_data

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <openapi_file.json> <path_prefix_1> [<path_prefix_2> ...]")
        sys.exit(1)

    openapi_file = sys.argv[1]
    path_prefixes = sys.argv[2:]

    new_openapi_data = filter_openapi_paths(openapi_file, path_prefixes)
    with open('filtered_openapi.json', 'w') as file:
        json.dump(new_openapi_data, file, indent=2)

    print("Filtered OpenAPI JSON saved as 'filtered_openapi.json'")

if __name__ == "__main__":
    main()
