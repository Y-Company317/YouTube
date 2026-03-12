import re
import sys
import os

def parse_and_fix(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    nodes = []
    
    # Regex for numbering: "1.", "1.1.", "1.1.1." etc.
    pattern = re.compile(r'^(\d+(?:\.\d+)*\.?)\s?(.*)')
    
    if not lines:
        return "", []

    root_title = lines[0].strip()
    
    last_main_node = None
    
    for i, line in enumerate(lines):
        if i == 0: continue
        
        line = line.strip()
        if not line: continue
        
        match = pattern.match(line)
        if match:
            num_str = match.group(1)
            content = match.group(2)
            
            clean_num = num_str.rstrip('.')
            parts = [int(p) for p in clean_num.split('.')]
            
            new_node = {
                'number_parts': parts,
                'number_str': num_str,
                'content': [content],
                'original_line': i + 1
            }
            nodes.append(new_node)
            
            # Check order
            if last_main_node:
                # Compare parts
                # If new < old, it's an interruption
                if new_node['number_parts'] < last_main_node['number_parts']:
                    # Interruption!
                    # Don't update last_main_node
                    pass
                else:
                    # Normal flow
                    last_main_node = new_node
            else:
                last_main_node = new_node
        else:
            # Continuation
            if last_main_node:
                last_main_node['content'].append(line)
    
    return root_title, nodes

def sort_nodes(nodes):
    return sorted(nodes, key=lambda x: x['number_parts'])

if __name__ == "__main__":
    filepath = "/Users/mikosawayuudai/Library/Mobile Documents/iCloud~md~obsidian/Documents/YouTube/YouTube/03_事業・案件/Y株式会社/スクール/イルカ/YouTube/YouTubeコンセプト.md"
    
    print(f"Reading {filepath}...")
    title, nodes = parse_and_fix(filepath)
    sorted_nodes = sort_nodes(nodes)
    
    print(f"Writing back to {filepath}...")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"- {title}\n")
        
        for node in sorted_nodes:
            depth = len(node['number_parts'])
            indent = "  " * depth # 2 spaces per level
            text = "".join(node['content'])
            # Ensure space between number and text if text exists and doesn't start with space
            # But we already captured space in regex? No, regex was \s?
            # If text is empty, no space.
            # If text is not empty, ensure space?
            # The original file had "1. 1.コンセプト" (space included in content?)
            # Regex: `^(\d+...)\s?(.*)`
            # If line was "1. 1.コンセプト", group 1 is "1.", group 2 is "1.コンセプト".
            # If line was "1.1. コアコンセプト", group 1 is "1.1.", group 2 is "コアコンセプト".
            # So the space after the dot is consumed by \s?.
            # We should probably add a space back for readability.
            
            # Check if text starts with space? No, strip() removed it.
            # So we should add a space.
            
            sep = " " if text else ""
            f.write(f"{indent}- {node['number_str']}{sep}{text}\n")
            
    print("Done.")
