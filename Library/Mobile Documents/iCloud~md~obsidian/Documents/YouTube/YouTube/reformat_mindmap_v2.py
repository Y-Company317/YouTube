import re
import sys

def parse_and_fix(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    nodes = []
    # We need a list of nodes to append to.
    # But we also need to track "current active node" for appending text.
    
    # We will store nodes in a list.
    # We will track `last_main_node` which is the node we append text to.
    
    # Logic:
    # 1. Parse line.
    # 2. If numbered:
    #    Check if it is "out of order" relative to `last_main_node`.
    #    If out of order:
    #       It is an interruption.
    #       Add it to `nodes`.
    #       Do NOT update `last_main_node`.
    #    Else:
    #       Add to `nodes`.
    #       Update `last_main_node` = this node.
    # 3. If text:
    #    Append to `last_main_node`.
    
    # Wait, what if the first node is out of order? (Unlikely)
    
    pattern = re.compile(r'^(\d+(?:\.\d+)*\.?)\s?(.*)')
    
    root_title = lines[0].strip()
    
    # Dummy start node to avoid None check?
    # No, first numbered line will set last_main_node.
    
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
    title, nodes = parse_and_fix(filepath)
    sorted_nodes = sort_nodes(nodes)
    
    # Check 1.2
    print("--- CHECKING 1.2 ---")
    for node in sorted_nodes:
        num = ".".join(map(str, node['number_parts']))
        if num == "1.2":
            print(f"[1.2]: {''.join(node['content'])}")
            
    # Output file content
    print("\n--- GENERATING FILE CONTENT ---")
    output_lines = []
    output_lines.append(f"- {title}")
    
    for node in sorted_nodes:
        depth = len(node['number_parts'])
        indent = "  " * depth
        # Join content with space or nothing?
        # The file had broken lines. "どのよ" + "うな" -> "どのような".
        # So we should join with empty string.
        # But what about "コンセプト" + "1.1."? No, those are separate nodes.
        # Inside a node: "理由として..." + "とスケール..." -> "理由として...とスケール...".
        # Sometimes there might be a space needed?
        # Japanese usually doesn't need spaces between lines.
        # But if it was English?
        # The file is Japanese.
        # I will join with empty string.
        
        text = "".join(node['content'])
        output_lines.append(f"{indent}- {node['number_str']} {text}")
        
    # Write to a temp file or just print first few
    for line in output_lines[:20]:
        print(line)
