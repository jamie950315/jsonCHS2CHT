# jsonCHS2CHT
A tool that can change CHS in json to CHT using OpenCC

## DynamicStringDistributor JSON Processor

## Overview
This script processes JSON files inside subfolders of the `DynamicStringDistributor` directory. It performs the following tasks:

1. **Convert Simplified Chinese to Traditional Chinese** using the OpenCC library.
2. **Apply advanced word replacements** based on predefined mappings.
3. **Process all `.json` and `.json.OLD000` files** inside subfolders ending with `.esl`, `.esm`, or `.esp`.
4. **Output a summary** listing folders where replacements were made, along with specific word changes.

## Installation
Before running the script, install the necessary dependency:

```bash
pip install opencc
```

## Usage
1. Place the script in the parent directory of `DynamicStringDistributor`.
2. Run the script using:

```bash
python jsonCHS2CHT.py
```

## Processing Details
- The script scans subfolders inside `DynamicStringDistributor`.
- If a folder ends with `.esl`, `.esm`, or `.esp`, it processes all `.json` and `.json.OLD000` files inside it.
- **All text** inside these JSON files is converted from Simplified Chinese to Traditional Chinese.
- **Word replacements** occur based on the following mappings:

  | Original | Replacement |
  |----------|------------|
  | 彆      | 別         |
  | 鬥篷    | 斗篷       |
  | 剛冰石  | 魔冰岩     |
  | 海爾根  | 聖地鎮     |
  | 天霜    | 天際       |
  | 麵具    | 面具       |

- After processing, the script **prints a list of folders** where replacements were made, along with the specific words that changed.

## Output Example
```
Folders with advanced replacements:
example.esl: 天霜->天際, 海爾根->聖地鎮
mod_data.esp: 鬥篷->斗篷, 麵具->面具
```

## Notes
- The script **modifies JSON files in place**.
- Only text values inside the JSON files are processed; structure and formatting remain unchanged.
- If no replacements occur, the script reports: `No advanced replacements were performed in any folder.`

## License
This script is open-source under MIT license and free to use and modify.

