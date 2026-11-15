import os
import re

targets = ['onion', 'kolar', 'chikkaballapur', 'bengaluru']
dirs_to_search = ['config.yaml', 'src', 'backend', 'frontend/src']

all_hits = []

def scan_file(fpath):
    try:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            for lno, line in enumerate(f, 1):
                line_lower = line.lower()
                matched = [t for t in targets if t in line_lower]
                if matched:
                    all_hits.append({
                        'file': fpath.replace('\\', '/'),
                        'line_num': lno,
                        'text': line.strip(),
                        'targets': matched
                    })
    except Exception as e:
        pass

for item in dirs_to_search:
    if os.path.isfile(item):
        scan_file(item)
    elif os.path.isdir(item):
        for root, dirs, files in os.walk(item):
            if any(x in root for x in ['node_modules', '.next', '__pycache__', '.git']):
                continue
            for file in files:
                if file.endswith(('.py', '.yaml', '.yml', '.ts', '.tsx', '.json', '.js', '.css', '.md')):
                    scan_file(os.path.join(root, file))

components = {
    'config.yaml': [],
    'src/ (pipeline, optimizer, advisor)': [],
    'backend/ (API, loaders, routers)': [],
    'frontend/src/ (pickers, components, pages)': [],
    'frontend/src/i18n/ (translations)': []
}

for hit in all_hits:
    f = hit['file']
    if f.startswith('config.yaml'):
        components['config.yaml'].append(hit)
    elif f.startswith('frontend/src/i18n'):
        components['frontend/src/i18n/ (translations)'].append(hit)
    elif f.startswith('frontend/src'):
        components['frontend/src/ (pickers, components, pages)'].append(hit)
    elif f.startswith('backend'):
        components['backend/ (API, loaders, routers)'].append(hit)
    elif f.startswith('src'):
        components['src/ (pipeline, optimizer, advisor)'].append(hit)

report = ['# Scope Diagnosis: Hard-Coded Onion & Target Mandis\n']
report.append('Generated: 2026-11-16. Audit of hard-coded references to `onion`, `Kolar`, `Chikkaballapur`, and `Bengaluru` across the codebase.\n')

for comp, hits in components.items():
    report.append(f'## {comp} ({len(hits)} occurrences)\n')
    for h in hits:
        matched_str = ", ".join(h["targets"])
        text_safe = h["text"].replace('`', "'")
        report.append(f'- **{h["file"]}:{h["line_num"]}** [{matched_str}]: `{text_safe}`')
    report.append('')

with open('reports/scope_diagnosis.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f'Done. Total hits: {len(all_hits)}')
