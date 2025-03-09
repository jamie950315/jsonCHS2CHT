import os
import json
import opencc

def advanced_replacement(text: str) -> (str, set):
    """
    Performs advanced replacements on the text and returns the modified text and a set of changes.
    Each change is recorded as a string in the format "old->new".
    """
    replacements = {
        "彆": "別",
        "鬥篷": "斗篷",
        "剛冰石": "魔冰岩",
        "海爾根": "聖地鎮",
        "天霜": "天際",
        "麵具": "面具"
    }
    changed = set()
    modified_text = text
    for old, new in replacements.items():
        if old in modified_text:
            modified_text = modified_text.replace(old, new)
            changed.add(f"{old}->{new}")
    return modified_text, changed

def convert_text(obj, converter, advanced=False):
    """
    Recursively converts all string values in a JSON object using OpenCC.
    If advanced is True, it also performs extra replacements and collects any replacement changes.
    
    Returns:
        A tuple: (converted_obj, set_of_replacements)
    """
    if isinstance(obj, str):
        # First convert using OpenCC.
        converted = converter.convert(obj)
        if advanced:
            replaced_text, changes = advanced_replacement(converted)
            return replaced_text, changes
        else:
            return converted, set()
    elif isinstance(obj, list):
        new_list = []
        changes_total = set()
        for item in obj:
            new_item, changes = convert_text(item, converter, advanced)
            new_list.append(new_item)
            changes_total.update(changes)
        return new_list, changes_total
    elif isinstance(obj, dict):
        new_dict = {}
        changes_total = set()
        for key, value in obj.items():
            if isinstance(key, str):
                new_key, changes_key = convert_text(key, converter, advanced)
            else:
                new_key, changes_key = key, set()
            new_value, changes_value = convert_text(value, converter, advanced)
            new_dict[new_key] = new_value
            changes_total.update(changes_key)
            changes_total.update(changes_value)
        return new_dict, changes_total
    else:
        return obj, set()

def process_json_file(file_path, converter, advanced=False):
    """
    Loads the JSON file, converts its content (and applies advanced replacements if enabled),
    then writes the updated data back to the same file.
    
    Returns:
        A set of advanced replacement changes that occurred in the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return set()

    converted_data, changes = convert_text(data, converter, advanced)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(converted_data, f, ensure_ascii=False, indent=4)
        print(f"Successfully processed: {file_path}")
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
    return changes

def process_files_in_folder(folder_path, converter, advanced=False):
    """
    Scans the specified folder for files ending in '.json' or '.json.OLD000' and processes each.
    
    Returns:
        A set of all advanced replacement changes that occurred in the folder.
    """
    aggregated_changes = set()
    found_file = False
    for filename in os.listdir(folder_path):
        if filename.endswith(".json") or filename.endswith(".json.OLD000"):
            found_file = True
            file_path = os.path.join(folder_path, filename)
            file_changes = process_json_file(file_path, converter, advanced)
            aggregated_changes.update(file_changes)
    if not found_file:
        print(f"No valid JSON file found in folder: {folder_path}")
    return aggregated_changes

def process_new_file_names(base_dir):
    """
    For every subfolder ending with '.esl', '.esm', or '.esp' in the base directory,
    this function scans for any file with a name ending in '.json' or '.json.OLD000' and processes it.
    
    Advanced replacements are applied for these folders.
    
    After processing, the script prints a list of subfolder names (and the changes made)
    where advanced replacement changed words.
    """
    converter = opencc.OpenCC('s2t')
    folders_with_changes = {}  # key: folder name, value: set of changes
    
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path) and (folder.endswith('.esl') or folder.endswith('.esm') or folder.endswith('.esp')):
            # Enable advanced replacements for all these subfolders.
            advanced_flag = True
            changes = process_files_in_folder(folder_path, converter, advanced_flag)
            if changes:
                folders_with_changes[folder] = changes
    
    if folders_with_changes:
        print("\nFolders with advanced replacements:")
        for folder, changes in folders_with_changes.items():
            changes_list = ", ".join(sorted(changes))
            print(f"{folder}: {changes_list}")
    else:
        print("\nNo advanced replacements were performed in any folder.")

def main():
    base_dir = "DynamicStringDistributor"  # Adjust this path if necessary.
    process_new_file_names(base_dir)

if __name__ == '__main__':
    main()
