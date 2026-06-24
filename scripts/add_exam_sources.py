#!/usr/bin/env python
"""Add examSource annotations to question-bank.json."""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('public/question-bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

exam_sources = {}

def add_source(qid, year):
    if qid not in exam_sources:
        exam_sources[qid] = set()
    exam_sources[qid].add(year)

# === TRANSLATION ===
trans_by_exam = {
    '21春夏': ['nucleosome','autoradiography','snRNPs','gel electrophoresis','trans-splicing',
               'nucleoid','C value paradox','lncRNA','spliceosome','噬菌体展示','终止子',
               '复制滑移','荧光共振能量转移','组蛋白','甲基化','表观遗传','同源重组',
               '拟核','解旋酶','操纵元','脱氧核糖核酸','开放阅读框','核苷酸','组氨酸','表观遗传学'],
    '21秋冬': ['alternative splicing','autoradiography','snRNPs','epigenetics','kinetochore',
               'trans-splicing','多顺反子','转录','功能基因组学','终止子','图位克隆'],
    '22春夏': ['gel electrophoresis','deoxyribonucleic acid','attenuator','epigenetics','mitosis',
               'centromere','autoradiography','enhancer','trans-activation domain','phosphorylation',
               'transforming factor','eucaryon','trans-splicing','codon preference','ubiquitination',
               '噬菌体','糖基化','操纵区','复制滑移','转座子','氨基酸','终止子','蛋白质组学','图位克隆','转录'],
    '23春夏': ['核小体','拟核','Meiosis','Eukaryote','Codon preference','trans-splicing',
               'C value paradox','Methylation','Ubiquitination','Transposon','spliceosome',
               '多顺反子','原位杂交','异染色质','噬菌体','蛋白质组学','表观遗传组学',
               '操纵位点','复制滑移','解旋酶'],
}
for q in bank['questions']:
    if q['type'] != 'translation': continue
    prompt = q['prompt']
    answer = (q.get('answerTerm','') + ' ' + (q.get('answerFullTerm') or '')).lower()
    chinese = q.get('chineseMeaning','').lower()
    all_text = f"{prompt} {answer} {chinese}".lower().replace(' ','').replace('-','')
    for year, terms in trans_by_exam.items():
        for term in terms:
            t = term.lower().replace(' ','').replace('-','')
            if t in all_text or t in prompt.replace(' ',''):
                add_source(q['id'], year)
                break

# === T/F ===
tf_by_exam = {
    '21春夏': ['sirna','sd','class iii','rrna','trna','trp','attenuator','aporepressor','fmet','cas13','mothering'],
    '21秋冬': ['translation initiation','class iii','rrna','trna'],
    '22春夏': ['lac','trp','replication','transcription'],
    '23春夏': ['blue-white','lacz'],
}
for q in bank['questions']:
    if q['type'] != 'true-false': continue
    all_text = (q['prompt'] + ' ' + q.get('explanation','')).lower()
    for year, topics in tf_by_exam.items():
        for topic in topics:
            if topic in all_text:
                add_source(q['id'], year)
                break

# === MC ===
# All 17 MC topics come from exam papers (deduced from exam paper keywords)
mc_map = {
    'multiple-choice-1-q-001': ['22春夏', '23春夏'],  # PCR inventor
    'multiple-choice-1-q-002': ['21春夏'],             # 35S
    'multiple-choice-2-q-003': ['21春夏'],             # fMet
    'multiple-choice-2-q-004': ['22春夏'],             # AUG=Met
    'multiple-choice-2-q-005': ['21春夏', '21秋冬'],   # SD sequence
    'multiple-choice-2-q-006': ['21春夏'],             # EF-Tu
    'multiple-choice-2-q-007': ['21秋冬'],             # Wobble
    'multiple-choice-3-q-008': ['21秋冬'],             # CRISPR/Cas13
    'multiple-choice-3-q-009': ['21春夏'],             # Dicer
    'multiple-choice-3-q-010': ['21秋冬'],             # Coding strand
    'multiple-choice-3-q-011': ['21春夏'],             # Ternary complex
    'multiple-choice-3-q-012': ['21秋冬'],             # Abortive transcription
    'multiple-choice-3-q-013': ['21春夏'],             # Splicing elements
    'multiple-choice-4-q-014': ['21春夏', '21秋冬'],   # Agrobacterium vir
    'multiple-choice-5-q-015': ['22春夏'],             # TF BD+AD
    'multiple-choice-5-q-016': ['23春夏'],             # Protein solubility
    'multiple-choice-5-q-017': ['21秋冬'],             # PCR primer
}
for qid, years in mc_map.items():
    for y in years:
        add_source(qid, y)

# === SA + Essay ===
sa_essay_map = {
    'short-answer-q-001': ['21春夏', '21秋冬'],
    'short-answer-q-002': ['21春夏', '21秋冬'],
    'short-answer-q-003': ['21春夏', '21秋冬'],
    'short-answer-q-004': ['22春夏'],
    'short-answer-q-005': ['23春夏'],
    'short-answer-q-006': ['21春夏', '23春夏'],
    'short-answer-q-007': ['22春夏'],
    'short-answer-q-008': ['21秋冬', '22春夏', '23春夏'],
    'short-answer-q-009': ['21秋冬'],
    'short-answer-q-010': ['23春夏'],
    'short-answer-q-011': ['21春夏', '21秋冬', '22春夏'],
    'short-answer-q-012': ['23春夏'],
    'short-answer-q-013': ['21春夏'],
    'short-answer-q-014': ['23春夏'],
    'short-answer-q-015': ['21春夏'],
    'short-answer-q-016': ['21秋冬'],
    'short-answer-q-017': ['22春夏'],
    'short-answer-q-018': ['21秋冬'],
    'short-answer-q-019': ['21春夏'],
    'short-answer-q-020': ['22春夏'],
    'short-answer-q-021': ['21秋冬'],
    'short-answer-q-022': ['21秋冬'],
    'short-answer-q-023': ['21秋冬'],
    'essay-q-024': ['21秋冬', '22春夏'],
    'essay-q-025': ['21春夏', '23春夏'],
    'essay-q-026': ['21秋冬', '23春夏'],
    'essay-q-027': ['22春夏'],
    'essay-q-028': ['21春夏', '21秋冬', '22春夏'],
    'essay-q-029': ['21春夏', '23春夏'],
    'essay-q-030': ['21秋冬'],
    'essay-q-031': ['21秋冬'],
}
for qid, years in sa_essay_map.items():
    for y in years:
        add_source(qid, y)

# Apply
count = 0
for q in bank['questions']:
    q['examSources'] = sorted(exam_sources.get(q['id'], []))
    if q['examSources']:
        count += 1

with open('public/question-bank.json', 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=2)

from collections import Counter
yc = Counter()
for q in bank['questions']:
    for y in q.get('examSources', []):
        yc[y] += 1
print(f'{count}/{len(bank["questions"])} questions annotated')
for y, c in yc.most_common():
    print(f'  {y}: {c}')
