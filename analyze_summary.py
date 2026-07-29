import re

with open(r'd:\Documents\Paradox Interactive\Europa Universalis IV\mod\YanShen Expansion\interface\MP.gfx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
i = 0
non_idea_EU4 = []  # no "idea_EU4" at all
ideas_EU4_only = []  # uses "ideas_EU4" (with s)
other_paths = []  # uses other paths entirely

while i < len(lines):
    line = lines[i]
    if re.match(r'^\s*spriteType\s*=\s*\{', line):
        start_line = i + 1
        brace_count = 0
        j = i
        block_lines = []
        while j < len(lines):
            block_lines.append(lines[j])
            brace_count += lines[j].count('{')
            brace_count -= lines[j].count('}')
            if brace_count == 0:
                break
            j += 1
        
        block = '\n'.join(block_lines)
        
        tex_match = re.search(r'texturefile\s*=\s*"([^"]+)"', block)
        if tex_match:
            tex_file = tex_match.group(1)
            name_match = re.search(r'name\s*=\s*"([^"]+)"', block)
            name = name_match.group(1) if name_match else "UNKNOWN"
            
            if 'idea_EU4' not in tex_file:
                # Does NOT contain "idea_EU4" (exact, no 's')
                if 'ideas_EU4' in tex_file:
                    ideas_EU4_only.append((start_line, name, tex_file))
                else:
                    other_paths.append((start_line, name, tex_file))
        i = j
    i += 1

with open(r'd:\Documents\Paradox Interactive\Europa Universalis IV\mod\YanShen Expansion\summary_results.txt', 'w', encoding='utf-8') as out:
    out.write("=" * 100 + "\n")
    out.write("分析结果：不包含 'idea_EU4'（无s）的 spriteType\n")
    out.write(f"总 spriteType 数: {len(non_idea_EU4) + len(ideas_EU4_only) + len(other_paths)}\n")
    out.write(f"其中包含 'idea_EU4'(精确) 被排除: 397\n")
    out.write(f"不包含 'idea_EU4'(精确) 的: {len(non_idea_EU4) + len(ideas_EU4_only) + len(other_paths)}\n\n")
    
    out.write("-" * 100 + "\n")
    out.write(f"【第一部分】使用 ideas_EU4 路径 (包含 's') 的 sprite: {len(ideas_EU4_only)} 个\n")
    out.write("-" * 100 + "\n")
    out.write(f"{'行号':>6} | {'Name':<45} | {'TextureFile'}\n")
    out.write("-" * 100 + "\n")
    for start_line, name, tex_file in ideas_EU4_only:
        out.write(f"{start_line:>6} | {name:<45} | {tex_file}\n")
    
    out.write("\n\n" + "-" * 100 + "\n")
    out.write(f"【第二部分】使用其他路径 (非 ideas_EU4 也非 idea_EU4) 的 sprite: {len(other_paths)} 个\n")
    out.write("-" * 100 + "\n")
    out.write(f"{'行号':>6} | {'Name':<45} | {'TextureFile'}\n")
    out.write("-" * 100 + "\n")
    for start_line, name, tex_file in other_paths:
        out.write(f"{start_line:>6} | {name:<45} | {tex_file}\n")
    
    out.write("\n\n=== 统计汇总 ===\n")
    out.write(f"不包含 'idea_EU4' 的 spriteType 总数: {len(non_idea_EU4) + len(ideas_EU4_only) + len(other_paths)}\n")
    out.write(f"  - 使用 ideas_EU4 路径（带 s）: {len(ideas_EU4_only)} 个\n")
    out.write(f"  - 使用其他路径（非 ideas_EU4 也非 idea_EU4）: {len(other_paths)} 个\n")

print("Done! Summary written to summary_results.txt")
print(f"Total non-idea_EU4: {len(non_idea_EU4) + len(ideas_EU4_only) + len(other_paths)}")
print(f"  - ideas_EU4 (with 's'): {len(ideas_EU4_only)}")
print(f"  - other paths: {len(other_paths)}")
