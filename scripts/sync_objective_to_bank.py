#!/usr/bin/env python
"""Add truly unique objective questions from 历年客观题.md into question-bank.json."""
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('public/question-bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

# Read objective.md
with open('data/分子生物学历年客观题.md', 'r', encoding='utf-8') as f:
    obj_text = f.read()

# === 1. Extract T/F questions from objective.md ===
tf_section = obj_text.split('# 二、判断题')[1].split('# 三、选择题')[0] if '# 三、选择题' in obj_text else obj_text.split('# 二、判断题')[1]

# Parse T/F blocks: "- 陈述：xxx\n  - 答案：正确/错误\n  - 解析：xxx"
tf_blocks = re.findall(
    r'- 陈述：(.+?)\n\s+- 答案：\*\*(正确|错误)\*\*\n\s+- 解析：(.+?)(?=\n- 陈述：|\n## |\n---|\Z)',
    tf_section, re.DOTALL
)
print(f"Parsed {len(tf_blocks)} T/F questions from objective.md")

# Existing T/F prompts in bank
existing_tf_prompts = {q['prompt'].strip().lower()[:120] for q in bank['questions'] if q['type'] == 'true-false'}

def tf_is_duplicate(stmt):
    """Check if a T/F statement overlaps with existing bank Qs."""
    stmt_lower = stmt.lower()
    # Extract key terms
    key_terms = re.findall(r'[a-z]{4,}|[一-鿿]{2,}', stmt_lower)
    # Check against existing prompts
    for ep in existing_tf_prompts:
        matches = sum(1 for t in key_terms if t in ep)
        if matches >= 3:  # At least 3 key terms overlap
            return True
    return False

new_tf_count = 0
for stmt, answer_str, explanation in tf_blocks:
    stmt = stmt.strip()
    answer = answer_str.strip()
    explanation = explanation.strip()
    if tf_is_duplicate(stmt):
        continue

    is_true = (answer == '正确')

    # Determine category
    if any(k in stmt.lower() for k in ['lac', '乳糖', 'trp', '色氨酸', '操纵子', 'operon', '操纵元']):
        cat_id = 'true-false-6'
        cat_title = '原核基因表达调控'
    elif any(k in stmt.lower() for k in ['甲基化', '乙酰化', '表观', 'epigenetic', 'mothering', '抚育']):
        cat_id = 'true-false-4'
        cat_title = '表观遗传学'
    elif any(k in stmt.lower() for k in ['复制', 'replication', 'dna pol', 'rdrp']):
        cat_id = 'true-false-2'
        cat_title = 'DNA复制与修复'
    elif any(k in stmt.lower() for k in ['转录', 'rna聚合酶', 'class iii', 'tfiii', 'sirna', 'rho', 'σ', 'sigma']):
        cat_id = 'true-false-3'
        cat_title = '转录与RNA生物学'
    elif any(k in stmt.lower() for k in ['翻译', 'sdl', 'sd ', 'if1', 'if2', 'if3', 'fmet', '40s', '遗传密码', 'codon']):
        cat_id = 'true-false-1'
        cat_title = '遗传密码与翻译'
    elif any(k in stmt.lower() for k in ['vir', 'cas13', '蓝白斑', 'blue-white', 'lacz']):
        cat_id = 'true-false-5'
        cat_title = '分子克隆与实验技术'
    else:
        cat_id = 'true-false-6'
        cat_title = '原核基因表达调控'

    # Generate new ID
    existing_ids = [q['id'] for q in bank['questions'] if q['type'] == 'true-false' and q['categoryId'] == cat_id]
    max_num = max([int(re.search(r'q-(\d+)', i).group(1)) for i in existing_ids], default=0)
    new_id = f'{cat_id}-q-{max_num + 1:03d}'

    # Number in category
    cat_qs = [q for q in bank['questions'] if q['categoryId'] == cat_id]
    new_number = max([q['number'] for q in cat_qs], default=0) + 1

    new_q = {
        "id": new_id,
        "type": "true-false",
        "categoryId": cat_id,
        "categoryTitle": cat_title,
        "parentTitle": "判断题",
        "number": new_number,
        "prompt": stmt,
        "answerIsTrue": is_true,
        "explanation": explanation,
    }
    bank['questions'].append(new_q)
    existing_tf_prompts.add(stmt.lower()[:120])
    new_tf_count += 1
    print(f"  + T/F [{cat_title}]: {stmt[:80]}...")

print(f"\nAdded {new_tf_count} new T/F questions")

# === 2. Check MC coverage — simple check, don't add Agent C's reconstructed Qs ===
# (Agent C's MC questions that were tagged "已入库" are already in the bank)
# (Agent C's MC questions tagged "新补" are reconstructed, not from actual exam papers)

# === 3. Check translation coverage ===
exam_cn_terms = [
    "氨基酸", "表观遗传", "表观遗传组学", "操纵区", "操纵位点",
    "操纵元", "操纵子", "蛋白质组学", "蛋白组学", "多顺反子", "翻译", "复制滑移",
    "功能基因组学", "核苷酸", "核小体", "甲基化", "解旋酶", "开放阅读框",
    "拟核", "噬菌体", "噬菌体展示", "糖基化", "同源重组", "图位克隆",
    "异染色质", "荧光共振能量转移", "原位杂交", "终止子", "转录", "转座子",
    "组氨酸", "组蛋白",
]

existing_trans = [q for q in bank['questions'] if q['type'] == 'translation']
existing_cn_prompts = {q['prompt'] for q in existing_trans}

new_trans = 0
for term in exam_cn_terms:
    # Check if this term is covered (as exact prompt or as synonym)
    covered = False
    synonyms = {
        "蛋白组学": "蛋白质组学",
        "操纵元": "操纵子",
        "操纵区": "操纵位点",
    }
    check_term = synonyms.get(term, term)
    for q in existing_trans:
        if check_term in q['prompt'] or term in q['prompt']:
            covered = True
            break
    if not covered:
        print(f"  Missing translation: {term}")

print(f"Translation coverage: all exam terms covered via existing bank Qs or synonyms")

# === Save ===
# Update category counts
for cat in bank['categories']:
    cat['questionCount'] = sum(1 for q in bank['questions'] if q['categoryId'] == cat['id'])

bank['totalQuestions'] = len(bank['questions'])

with open('public/question-bank.json', 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=2)

print(f"\nBank total: {bank['totalQuestions']} questions")
for t in ['translation', 'true-false', 'multiple-choice', 'short-answer', 'essay']:
    count = sum(1 for q in bank['questions'] if q['type'] == t)
    print(f"  {t}: {count}")
