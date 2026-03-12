import re
import sys

def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    nodes = []
    current_node = None
    
    # Regex for numbering: "1.", "1.1.", "1.1.1." etc.
    # It seems to always end with a dot and then space?
    # Or sometimes just dot?
    # Line 2: "1. 1.コンセプト" -> "1."
    # Line 3: "1.1. コアコンセプト" -> "1.1."
    # Line 57: "1.1.3.4. 再生回数を..." -> "1.1.3.4."
    
    pattern = re.compile(r'^(\d+(?:\.\d+)*\.?)\s?(.*)')

    root_title = lines[0].strip()
    # Start from line 1 (index 1)
    
    # We'll store raw lines first to handle the "continuation" logic
    # But wait, if lines are interleaved, simple continuation is wrong.
    # Let's first try simple continuation and see the result.
    
    for i, line in enumerate(lines):
        if i == 0: continue # Skip title for now
        
        line = line.strip()
        if not line: continue
        
        match = pattern.match(line)
        if match:
            # It's a numbered line
            num_str = match.group(1)
            content = match.group(2)
            
            # Normalize number string (remove trailing dot for sorting/depth)
            # But keep original for display if needed? 
            # Actually, we want to reconstruct the hierarchy.
            
            # Remove trailing dot if present for parsing
            clean_num = num_str.rstrip('.')
            parts = [int(p) for p in clean_num.split('.')]
            
            current_node = {
                'number_parts': parts,
                'number_str': num_str,
                'content': [content],
                'original_line': i + 1
            }
            nodes.append(current_node)
        else:
            # Continuation line
            if current_node:
                current_node['content'].append(line)
            else:
                # Content before any number? (Shouldn't happen based on file read)
                pass

    return root_title, nodes

def sort_nodes(nodes):
    return sorted(nodes, key=lambda x: x['number_parts'])

def print_nodes(root_title, nodes):
    print(f"- {root_title}")
    
    for node in nodes:
        depth = len(node['number_parts'])
        indent = "  " * depth # Level 1 -> 2 spaces (inside root)
        
        # Join content
        text = "".join(node['content'])
        
        # Output
        # We keep the number string in the text to preserve "content" as requested?
        # User said "内容は変更しないでください" (Don't change content).
        # But for a mind map, usually you want the text to be the node content.
        # The number is structural.
        # If I output "- 1.1. コアコンセプト", the node text is "1.1. コアコンセプト".
        # This is fine.
        
        print(f"{indent}- {node['number_str']} {text}")

if __name__ == "__main__":
    filepath = "/Users/mikosawayuudai/Library/Mobile Documents/iCloud~md~obsidian/Documents/YouTube/YouTube/03_事業・案件/Y株式会社/スクール/イルカ/YouTube/YouTubeコンセプト.md"
    title, nodes = parse_file(filepath)
    sorted_nodes = sort_nodes(nodes)
    
    # Let's inspect specific nodes to check for the interleaving issue
    # 1.2 and 1.1.3.4
    
    print("--- CHECKING SPECIFIC NODES ---")
    for node in sorted_nodes:
        num = ".".join(map(str, node['number_parts']))
        if num == "1.2":
            print(f"[1.2]: {''.join(node['content'])}")
        if num == "1.1.3.4":
            print(f"[1.1.3.4]: {''.join(node['content'])}")
        if num == "1.1.2.1.7":
             print(f"[1.1.2.1.7]: {''.join(node['content'])}")
             
    print("\n--- FULL OUTPUT PREVIEW (First 50 lines) ---")
    print(f"- {title}")
    count = 0
    for node in sorted_nodes:
        depth = len(node['number_parts'])
        indent = "  " * depth
        text = "".join(node['content'])
        print(f"{indent}- {node['number_str']} {text}")
        count += 1
        if count > 50: break
