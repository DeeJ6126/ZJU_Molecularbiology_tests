#!/usr/bin/env python
"""Update question-bank.json: add missing objective Qs, replace subjective answers."""
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('public/question-bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

# === Step 1: Check coverage of exam objective questions ===
# Translation terms from exams (55 total)
exam_en_terms = {
    "alternative splicing", "attenuator", "autoradiography", "C value paradox",
    "centromere", "codon preference", "codon bias", "deoxyribonucleic acid",
    "enhancer", "epigenetics", "eucaryon", "eukaryote", "gel electrophoresis",
    "kinetochore", "lncRNA", "meiosis", "methylation", "mitosis",
    "nucleoid", "nucleosome", "phosphorylation", "snRNPs", "snRNP",
    "spliceosome", "trans-activation domain", "transforming factor",
    "transposon", "trans-splicing", "ubiquitination",
}

exam_cn_terms = {
    "氨基酸", "表观遗传", "表观遗传学", "表观遗传组学", "操纵区", "操纵位点",
    "操纵元", "操纵子", "蛋白质组学", "蛋白组学", "多顺反子", "翻译", "复制滑移",
    "功能基因组学", "核苷酸", "核小体", "甲基化", "解旋酶", "开放阅读框",
    "拟核", "噬菌体", "噬菌体展示", "糖基化", "同源重组", "图位克隆",
    "异染色质", "荧光共振能量转移", "原位杂交", "终止子", "转录", "转座子",
    "组氨酸", "组蛋白",
}

# Check existing translation Qs
existing_trans = [q for q in bank['questions'] if q['type'] == 'translation']
existing_prompts = {q['prompt'].strip().lower() for q in existing_trans}
existing_answers = set()
for q in existing_trans:
    for a in q.get('acceptableAnswers', []):
        existing_answers.add(a.lower().strip())
    if q.get('answerTerm'):
        existing_answers.add(q['answerTerm'].lower().strip())
    if q.get('answerFullTerm'):
        existing_answers.add(q['answerFullTerm'].lower().strip())

missing_en = []
for term in exam_en_terms:
    found = False
    for q in existing_trans:
        # Check if any acceptable answer contains this term
        all_text = ' '.join(q.get('acceptableAnswers', []) + [q.get('answerTerm', ''), q.get('answerFullTerm') or '']).lower()
        if term.lower() in all_text:
            found = True
            break
    if not found:
        missing_en.append(term)

missing_cn = []
for term in exam_cn_terms:
    found = False
    for q in existing_trans:
        if term in q['prompt'] or term in q.get('chineseMeaning', ''):
            found = True
            break
    if not found:
        missing_cn.append(term)

print(f"=== Translation coverage ===")
print(f"Existing translation Qs: {len(existing_trans)}")
print(f"Exam English terms: {len(exam_en_terms)}, Missing: {len(missing_en)}")
if missing_en:
    print(f"  Missing EN: {missing_en}")
print(f"Exam Chinese terms: {len(exam_cn_terms)}, Missing: {len(missing_cn)}")
if missing_cn:
    print(f"  Missing CN: {missing_cn}")

# Check T/F coverage
tf_existing = [q for q in bank['questions'] if q['type'] == 'true-false']
tf_prompts = {q['prompt'].strip().lower()[:80] for q in tf_existing}
print(f"\n=== T/F coverage ===")
print(f"Existing T/F Qs: {len(tf_existing)}")

# Key T/F topics from exams that should be in bank
exam_tf_topics = [
    "SD序列", "Shine-Dalgarno", "Class III", "TFIII", "rRNA", "tRNA",
    "siRNA", "trp", "attenuator", "apo repressor", "RdRP", "fMet", "Met",
    "mothering", "mother", "表观遗传", "Cas13", "vir", "蓝白斑",
    "lac", "乳糖", "CAP", "cAMP", "别乳糖",
]
missing_tf_topics = []
for topic in exam_tf_topics:
    found = any(topic.lower() in p for p in tf_prompts)
    if not found:
        missing_tf_topics.append(topic)
print(f"T/F topics from exams not in bank: {missing_tf_topics}")

# Check MC coverage
mc_existing = [q for q in bank['questions'] if q['type'] == 'multiple-choice']
print(f"\n=== MC coverage ===")
print(f"Existing MC Qs: {len(mc_existing)}")

# === Step 2: Add missing objective questions ===
# For translation: terms already well-covered, most "missing" are synonyms
# For T/F: need to add lac operon, blue-white screening, etc.
# For MC: Agent C already identified which are new

missing_count = 0

# Add a few key missing T/F questions
new_tf_qs = [
    {
        "id": "true-false-6-q-014",
        "type": "true-false",
        "categoryId": "true-false-6",
        "categoryTitle": "原核基因表达调控",
        "parentTitle": "判断题",
        "number": 14,
        "prompt": "In the lac operon, allolactose acts as an inducer by binding the repressor, causing it to dissociate from the operator and turn on transcription.",
        "answerIsTrue": True,
        "explanation": "别乳糖（allolactose）作为诱导物与lac阻遏蛋白结合，使其从操纵区解离，从而开启操纵子转录（MB7第43页）"
    },
    {
        "id": "true-false-6-q-015",
        "type": "true-false",
        "categoryId": "true-false-6",
        "categoryTitle": "原核基因表达调控",
        "parentTitle": "判断题",
        "number": 15,
        "prompt": "The lac operon is efficiently expressed when both glucose and lactose are present.",
        "answerIsTrue": False,
        "explanation": "lac操纵子在葡萄糖存在时受分解代谢物阻遏：葡萄糖→cAMP浓度低→CAP-cAMP复合物不能有效结合启动子→即使有乳糖诱导，转录也处于低水平（MB7第48页）"
    },
    {
        "id": "true-false-6-q-016",
        "type": "true-false",
        "categoryId": "true-false-6",
        "categoryTitle": "原核基因表达调控",
        "parentTitle": "判断题",
        "number": 16,
        "prompt": "In the Trp operon, the aporepressor is active and can bind to the operator even in the absence of tryptophan.",
        "answerIsTrue": False,
        "explanation": "辅阻遏蛋白（aporepressor）本身无活性，必须与色氨酸结合后才能变为有活性的阻遏蛋白结合操纵区。低色氨酸时无阻遏（MB7第52页）"
    },
]

# Add category for 原核基因表达调控 if not exists
cat_ids = {c['id'] for c in bank['categories']}
if 'true-false-6' not in cat_ids:
    bank['categories'].append({
        "id": "true-false-6",
        "type": "true-false",
        "title": "原核基因表达调控",
        "parentTitle": "判断题",
        "questionCount": 0,
    })

# Check which TF IDs already exist
existing_tf_ids = {q['id'] for q in bank['questions'] if q['type'] == 'true-false'}
for new_q in new_tf_qs:
    if new_q['id'] not in existing_tf_ids:
        bank['questions'].append(new_q)
        missing_count += 1
        print(f"Added T/F: {new_q['id']} - {new_q['prompt'][:80]}...")

# Update category counts
for cat in bank['categories']:
    cat['questionCount'] = sum(1 for q in bank['questions'] if q['categoryId'] == cat['id'])

# === Step 3: Replace subjective answers from 分子生物学历年主观题.md ===
with open('data/分子生物学历年主观题.md', 'r', encoding='utf-8') as f:
    subj_text = f.read()

# Parse Q&A pairs from subjective md
# Pattern: ### QN. title ... **答案：** ... **来源：** ...
q_pattern = re.compile(
    r'### Q(\d+)\.\s+(.+?)\n\n\*\*答案：\*\*\n(.*?)\n\n\*\*来源：\*\*',
    re.DOTALL
)

subj_answers = {}
for m in q_pattern.finditer(subj_text):
    qnum = int(m.group(1))
    title = m.group(2).strip()
    answer = m.group(3).strip()
    subj_answers[qnum] = {'title': title, 'answer': answer}

print(f"\nParsed {len(subj_answers)} subjective answers from 主观题.md")

# Map subjective Q numbers to question-bank IDs
# Q1-Q23 = short-answer, Q24-Q31 = essay
sa_qs = [q for q in bank['questions'] if q['type'] == 'short-answer']
essay_qs = [q for q in bank['questions'] if q['type'] == 'essay']

# Build lookup by topic keyword matching
import difflib

updated_sa = 0
updated_essay = 0

def find_best_match(title, candidates):
    """Find best matching bank question by prompt similarity."""
    best_score = 0
    best_q = None
    # Key terms from Chinese title that should map to English content
    title_lower = title.lower()
    for q in candidates:
        q_text = (q['prompt'] + ' ' + q.get('referenceAnswer', '')).lower()
        score = 0
        # Use keyword co-occurrence
        keywords_map = [
            # Chinese keyword -> English keywords to look for
            (['dna复制', '三种方式', '类型'], ['dna replication', 'types of dna replication', 'three types']),
            (['mrna剪接', 'splicing'], ['splicing', 'pre-mrna splicing']),
            (['mirna', '合成'], ['mirna', 'synthesis', 'biogenesis']),
            (['加帽', 'capping'], ['capping', '5\' cap', 'cap structure']),
            (['化学键', '水解酶'], ['chemical bond', 'nucleotide', 'nuclease', 'phosphodiester']),
            (['class ii', '转录起始', 'pic', 'preinitiation'], ['class ii', 'preinitiation', 'pic', 'transcription initiation']),
            (['pol i', 'rna聚合酶'], ['rna polymerase', 'pol iv', 'pol v']),
            (['翻译起始', '真核', '原核'], ['translation initiation', 'eukaryotic', 'prokaryotic']),
            (['30s', '起始复合物'], ['30s initiation', '30s complex', 'initiation complex']),
            (['翻译', 'rna', '生物学功能'], ['rna', 'translation', 'mrna', 'trna', 'rrna', 'function']),
            (['dna', '蛋白质', '互作', '检测'], ['dna-protein interaction', 'dna binding protein']),
            (['蛋白质', '蛋白', '互作', '检测', 'ab'], ['protein-protein interaction', 'protein interaction']),
            (['酵母双杂交', 'y2h'], ['yeast two-hybrid', 'y2h']),
            (['改变', '蛋白活性', '修饰'], ['modification', 'post-translational', 'protein activity', 'phosphorylation']),
            (['导入', '质粒', '基因', '载体'], ['insert', 'plasmid', 'cloning', 'vector', 'gene into']),
            (['loss of function', '功能丧失', '基因功能丧失', '敲除', '敲降'], ['loss of function', 'knockout', 'knockdown', 'gene function']),
            (['tags', '标签'], ['tag', 'fusion', 'affinity', 'his']),
            (['植物', '农杆菌', '转入', '质粒'], ['plants', 'agrobacterium', 't-dna', 'transformation']),
            (['着丝粒', 'centromere'], ['centromere', 'kinetochore']),
            (['色氨酸', 'trp', '操纵子', '调节'], ['trp', 'tryptophan', 'operon', 'regulation']),
            (['组氨酸', '前导', 'his'], ['histidine', 'leader', 'attenuation']),
            (['表观遗传', 'epigenetic'], ['epigenetic', 'inheritance']),
            (['蘑菇毒素', 'amanitin'], ['amanitin', 'mushroom', 'toxin']),
            (['griffith', 'hershey', '遗传物质'], ['griffith', 'hershey', 'genetic material', 'dna']),
            (['端粒', 'telomere'], ['telomere', 'telomerase']),
            (['衰减子', 'attenuator', 'trp操纵子', '看图'], ['attenuator', 'trp operon', 'attenuation']),
            (['sirna', 'mirna', '区别', '不同'], ['sirna', 'mirna', 'difference', 'comparison']),
            (['盐', '诱导', '胁迫'], ['salt', 'stress', 'induc', 'expression']),
            (['可变剪接', 'exon', 'alternative splicing'], ['alternative splicing', 'exon', 'isoform']),
            (['内含子', 'intron', '验证'], ['intron', 'validation', 'verify']),
            (['同尾酶', '载体构建', 'sal i', 'xho i'], ['vector', 'isocaudomer', 'sal i', 'xho i', 'restriction']),
        ]
        for cn_keywords, en_keywords in keywords_map:
            cn_match = any(k in title_lower for k in cn_keywords)
            en_match = any(k in q_text for k in en_keywords)
            if cn_match and en_match:
                score += 1
        if score > best_score:
            best_score = score
            best_q = q
    return best_q, best_score / max(len([k for k in keywords_map if any(kw in title_lower for kw in k[0])]), 1) if best_score > 0 else (best_q, 0)

for qnum, data in subj_answers.items():
    if qnum <= 23:
        candidates = sa_qs
        qtype = 'short-answer'
    else:
        candidates = essay_qs
        qtype = 'essay'

    best_q, score = find_best_match(data['title'], candidates)
    if best_q and score > 0.3:
        best_q['referenceAnswer'] = data['answer']
        if qtype == 'short-answer':
            updated_sa += 1
        else:
            updated_essay += 1
    elif best_q:
        print(f"  Weak match for Q{qnum} ({data['title'][:50]}): {best_q['prompt'][:50]} (score={score:.2f})")

print(f"\nUpdated short-answer: {updated_sa}/{len(sa_qs)}")
print(f"Updated essay: {updated_essay}/{len(essay_qs)}")

# === Save ===
bank['totalQuestions'] = len(bank['questions'])
with open('public/question-bank.json', 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=2)

print(f"\nTotal questions in bank: {bank['totalQuestions']}")
print(f"  Translation: {sum(1 for q in bank['questions'] if q['type']=='translation')}")
print(f"  True-false: {sum(1 for q in bank['questions'] if q['type']=='true-false')}")
print(f"  Multiple-choice: {sum(1 for q in bank['questions'] if q['type']=='multiple-choice')}")
print(f"  Short-answer: {sum(1 for q in bank['questions'] if q['type']=='short-answer')}")
print(f"  Essay: {sum(1 for q in bank['questions'] if q['type']=='essay')}")
print(f"Added {missing_count} new objective questions")
print("Done!")
