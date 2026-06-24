#!/usr/bin/env python
"""Convert 分子生物学历年主观题.md to Xmind-friendly pure-bullet format.

Rules:
1. EVERY line must start with "- " (no plain text lines)
2. Indentation is strictly progressive (0, 4, 8, 12, 16 spaces)
3. Key scoring terms are bolded with **...**
"""

import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/分子生物学历年主观题.md', 'r', encoding='utf-8') as f:
    text = f.read()

out = []

def bullet(level, text):
    prefix = '    ' * level + '- '
    return prefix + text

BOLD_TERMS = [
    r'Dicer', r'Drosha', r'Exportin-?5', r'RISC', r'DnaB', r'Cas9', r'Cas13',
    r'EF-Tu', r'EF-G', r'EF-Ts', r'IF[123](?!\d)', r'eIF[2345](?!\d)', r'eIF4[AF]',
    r'RNA聚合酶[IV]+', r'Pol [IV]+',
    r'TFII[ABCDEFH]', r'TBP', r'TAF', r'CENP-A', r'TRF2',
    r'端粒酶', r'Telomerase', r'DNA聚合酶[I]+', r'DNase', r'RNase',
    r'核酸酶', r'解旋酶', r'Helicase', r'N-糖苷酶', r'DNA glycosylase',
    r'逆转录酶', r'reverse transcriptase', r'HAT', r'HDAC', r'DNMT', r'Dnmt3',
    r'鸟苷酸转移酶', r'guanylyl transferase', r'甲基转移酶', r'肽基转移酶',
    r'\bU[1-6]\b', r'snRNP', r'SD序列', r'Shine-Dalgarno', r'Kozak序列',
    r'TATA box', r'衰减子', r'attenuator', r'衰减作用', r'Attenuation',
    r'反馈阻遏', r'阻遏蛋白', r'辅阻遏物', r'同尾酶', r'Isocaudomers',
    r'粘性末端', r'sticky ends', r'平末端', r'blunt ends',
    r't-环', r't-loop', r'套索', r'lariat', r'分支点', r'branch point',
    r'茎环', r'hairpin', r'发夹',
    r'\b70S\b', r'\b80S\b', r'\b30S\b', r'\b50S\b', r'\b40S\b', r'\b60S\b',
    r"5' cap", r"3' polyA", r"5'-5'三磷酸",
    r'ChIP', r'EMSA', r'Y2H', r'Co-IP', r'GST Pull-down',
    r'qRT-PCR', r'Northern blot', r'Southern blot', r'Western blot',
    r'RT-PCR', r'CRISPR', r'RNAi', r'PTGS', r'RdRp', r'Ago2',
    r'磷酸化', r'Phosphorylation', r'乙酰化', r'Acetylation',
    r'泛素化', r'Ubiquitination', r'甲基化', r'Methylation',
    r'糖基化', r'Glycosylation', r'SUMO化',
    r'fMet', r'N-甲酰甲硫氨酸', r'甲硫氨酸', r'\bMet\b',
    r'根癌农杆菌', r'Agrobacterium tumefaciens',
    r'T-DNA', r'Ti质粒', r'vir基因', r'双元质粒', r'Binary plasmid',
    r'σ因子', r'sigma factor', r'全酶', r'holoenzyme', r'核心酶', r'core enzyme',
    r'磷酸二酯键', r'糖苷键', r'氢键',
    r'Cap [012]型', r'Cap [012]',
    r'NHEJ', r'DSB', r'Indel',
    r'Nuclease', r'Helicase',
]

def apply_bold(text):
    for term in BOLD_TERMS:
        pattern = re.compile(r'(?<!\*\*)(' + term + r')(?!\*\*)', re.IGNORECASE)
        text = pattern.sub(r'**\1**', text)
    text = re.sub(r'\*\*met\*\*hyl', 'methyl', text)
    text = re.sub(r'\*\*met\*\*', 'met', text)
    return text

# Parse questions
lines = text.split('\n')
questions = {}
current_q = None
current_title = ''
current_content = []

for line in lines:
    s = line.strip()
    if not s or s == '---':
        continue
    if s.startswith('**来源：') or s == '**答案：**':
        continue
    if re.match(r'^# [三四]、', s):
        continue

    m = re.match(r'^### Q(\d+)\.\s+(.+)', s)
    if m:
        if current_q:
            questions[current_q] = {'title': current_title, 'content': current_content}
        current_q = int(m.group(1))
        current_title = m.group(2).strip()
        current_content = []
        continue

    if current_q:
        current_content.append(s)

if current_q:
    questions[current_q] = {'title': current_title, 'content': current_content}

def process_q(qdata, level=1):
    """Process one question into structured bullets."""
    out.append(bullet(level, apply_bold(re.sub(r'\*\*', '', qdata['title']))))

    full_text = ' '.join(qdata['content'])
    full_text = re.sub(r'\*\*(.+?)\*\*', r'\1', full_text)
    full_text = re.sub(r'\*(.+?)\*', r'\1', full_text)
    full_text = re.sub(r'`(.+?)`', r'\1', full_text)

    # Split into major chunks
    parts = re.split(r'(?=(?:[（(]\d+[）)]|\d+\.\s+(?=[A-Z一-鿿])|第[一二三四五六七八九十\d]+步[：:]))', full_text)

    # Expand inline sub-lists (text with " - xxx" patterns inside)
    expanded = []
    for part in parts:
        part = part.strip()
        # Detect inline "- xxx" sub-items (like "- Cap 0型：xxx - Cap 1型：xxx")
        sub_items = re.split(r'\s*[-–—]\s+(?=[A-Z一-鿿a-zA-Z（(])', part)
        if len(sub_items) > 1 and all(len(s) > 5 for s in sub_items):
            expanded.extend(s.strip() for s in sub_items if s.strip())
        else:
            expanded.append(part)

    # Remove redundant wrapper phrases
    wrappers = [
        r'^DNA复制有三种方式[：:]?\s*$',
        r'^miRNA的合成过程包括以下步骤[：:]?\s*$',
        r'^翻译过程中需要以下三种RNA[：:]?\s*$',
        r'^在植物中，除[^外]+之外，还存在\S+额外的RNA聚合酶[：:]?\s*$',
        r'^剪接过程分为两步转酯反应[：:]?\s*$',
    ]

    parts = []
    for item in expanded:
        is_wrapper = False
        for w in wrappers:
            if re.match(w, item):
                is_wrapper = True
                break
        if not is_wrapper:
            parts.append(item)

    # Natural sub-headers that should be at level+1
    sub_headers = [
        r'^(?:三种类型|生物学作用|三种酶的核心区别|装配顺序（四步）|加帽的合成过程（四步）|核心区别)[：:]?\s*$',
        r'^(?:原核翻译起始（6步）|真核翻译起始|原核翻译起始|真核翻译起始：)[：:]?\s*$',
        r'^(?:合成过程|生物学作用|四、如何避免酶切错误|三、操作步骤|二、解决方案|一、问题分析)[：:]?\s*$',
    ]

    for part in parts:
        part = part.strip().rstrip('；;，,。．')
        if not part or len(part) < 3:
            continue

        # Sub-header patterns (output at level+1 as a group heading)
        is_subheader = False
        for sh in sub_headers:
            if re.match(sh, part):
                clean = re.sub(r'[：:]$', '', part)
                out.append(bullet(level+1, apply_bold(clean)))
                is_subheader = True
                break
        if is_subheader:
            continue

        # Numbered item: "1. xxx"
        m = re.match(r'^(\d+)\.\s+(.+)', part)
        if m:
            text = m.group(2).strip().rstrip('；;，,。．')
            cm = re.match(r'^(.{2,30})[：:]\s*(.+)', text)
            if cm and len(cm.group(2)) > 10:
                out.append(bullet(level+1, apply_bold(f'{cm.group(1)}：{cm.group(2)}')))
            else:
                out.append(bullet(level+1, apply_bold(text)))
            continue

        # Parenthesized item: "（1）xxx"
        m = re.match(r'^[（(](\d+)[）)]\s*(.+)', part)
        if m:
            text = m.group(2).strip().rstrip('；;，,。．')
            out.append(bullet(level+1, apply_bold(f'({m.group(1)}) {text}')))
            continue

        # Step header: "第X步：xxx"
        m = re.match(r'^第([一二三四五六七八九十\d]+)步[：:]\s*(.+)', part)
        if m:
            text = m.group(2).strip().rstrip('；;，,。．')
            out.append(bullet(level+1, apply_bold(f'第{m.group(1)}步：{text}')))
            continue

        # Short heading: long text pattern
        m = re.match(r'^(.{2,40})[：:]\s*(.+)', part)
        if m and len(m.group(1)) < 35:
            label = m.group(1).strip()
            rest = m.group(2).strip().rstrip('；;，,。．')
            subparts = re.split(r'(?=(?:[（(]\d+[）)]|①|②|③|④|⑤|⑥|⑦|⑧|⑨))', rest)
            if len(subparts) > 1:
                out.append(bullet(level+1, apply_bold(f'{label}：')))
                for sp in subparts:
                    sp = sp.strip().rstrip('；;，,。．')
                    if sp:
                        out.append(bullet(level+2, apply_bold(sp)))
            else:
                out.append(bullet(level+1, apply_bold(f'{label}：{rest}')))
            continue

        # Default
        if len(part) > 5:
            out.append(bullet(level+1, apply_bold(part)))

# Output
out.append(bullet(0, '简答题'))
for qnum in sorted(questions.keys()):
    if qnum <= 23:
        process_q(questions[qnum], level=1)

out.append(bullet(0, '分析论述题'))
for qnum in sorted(questions.keys()):
    if qnum >= 24:
        process_q(questions[qnum], level=1)

result = '\n'.join(out)
result = re.sub(r'\*\*met\*\*hyl', 'methyl', result)
result = re.sub(r'\*\*met\*\*', 'met', result)

with open('data/分子生物学历年主观题_xmind.md', 'w', encoding='utf-8') as f:
    f.write(result)

print(f'Written: {len(result)} chars, {len(result.splitlines())} lines')
print()
# Show sample
for l in result.split('\n')[:45]:
    print(l)
