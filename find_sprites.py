import re

with open(r'd:\Documents\Paradox Interactive\Europa Universalis IV\mod\YanShen Expansion\interface\MP.gfx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
i = 0
results = []
debug_count_total = 0
debug_count_excluded = 0

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
        debug_count_total += 1
        
        tex_match = re.search(r'texturefile\s*=\s*"([^"]+)"', block)
        if tex_match:
            tex_file = tex_match.group(1)
            if 'idea_EU4' not in tex_file:
                name_match = re.search(r'name\s*=\s*"([^"]+)"', block)
                if name_match:
                    name = name_match.group(1)
                    results.append((start_line, name, tex_file))
            else:
                debug_count_excluded += 1
        i = j
    i += 1

# Write to a file instead of stdout to avoid truncation
with open(r'd:\Documents\Paradox Interactive\Europa Universalis IV\mod\YanShen Expansion\output_results.txt', 'w', encoding='utf-8') as out:
    out.write(f'Total spriteType blocks found: {debug_count_total}\n')
    out.write(f'Excluded (contain idea_EU4): {debug_count_excluded}\n')
    out.write(f'Included (no idea_EU4): {len(results)}\n\n')
    out.write(f'{"Line":>8} | {"Name":<45} | {"TextureFile"}\n')
    out.write('-' * 120 + '\n')
    for start_line, name, tex_file in results:
        out.write(f'{start_line:>8} | {name:<45} | {tex_file}\n')

print('Done! Results written to output_results.txt')
print(f'Total: {debug_count_total}, Excluded: {debug_count_excluded}, Included: {len(results)}')
