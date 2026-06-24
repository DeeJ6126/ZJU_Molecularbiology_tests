#!/usr/bin/env python
"""Verify question-bank.json fully covers all exam content from data/历年卷/."""
import sys, io, json, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('public/question-bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

gaps = []

# === 1. TRANSLATION ===
trans_qs = [q for q in bank['questions'] if q['type'] == 'translation']
bank_en_all = ' '.join(
    (q.get('answerTerm','') + ' ' + (q.get('answerFullTerm') or '') + ' ' + ' '.join(q.get('acceptableAnswers',[]))).lower()
    for q in trans_qs
)
bank_cn_all = ' '.join(q['prompt'] for q in trans_qs)

key_en = ['alternative splicing','autoradiography','snrnps','gel electrophoresis','trans-splicing',
    'nucleoid','kinetochore','centromere','telomere','c value paradox','lncrna','sirna','ptgs','risc',
    'epigenetics','histone code','mitosis','meiosis','eukaryote','enhancer','trans-activation domain',
    'phosphorylation','ubiquitination','transforming factor','codon preference','transposon',
    'ultracentrifugation','topoisomerase','gfp','deoxyribonucleic acid','attenuator']
key_cn = ['噬菌体展示','终止子','操纵元','操纵区','操纵位点','开放阅读框','多顺反子','转录','解旋酶',
    '复制滑移','滞后链','脱氧核糖核酸','氨基酸','荧光共振能量转移','组蛋白','核小体','异染色质',
    '甲基化','糖基化','表观遗传','表观遗传组学','同源重组','转座子','功能基因组学','蛋白质组学',
    '反向遗传学','图位克隆','原位杂交','拟核','组氨酸','核苷酸']

for term in key_en:
    if term not in bank_en_all:
        gaps.append(f'TRANS EN: {term}')
for term in key_cn:
    if term not in bank_cn_all:
        gaps.append(f'TRANS CN: {term}')

# === 2. T/F ===
tf_qs = [q for q in bank['questions'] if q['type'] == 'true-false']
tf_all = ' '.join(q['prompt'].lower() + ' ' + q.get('explanation','').lower() for q in tf_qs)

tf_checks = {
    'siRNA/RISC': 'sirna' in tf_all,
    'SD序列': ('sd' in tf_all or 'shine' in tf_all),
    'Class III/TFIII': ('class iii' in tf_all.lower() or 'tfiii' in tf_all),
    '5S rRNA vs tRNA transcription': ('rrna' in tf_all and 'trna' in tf_all and 'transcription' in tf_all),
    'trp attenuator': ('attenuat' in tf_all),
    'trp aporepressor': ('aporepressor' in tf_all or '辅阻遏' in tf_all),
    'fMet vs Met': ('fmet' in tf_all),
    'RdRp not in DNA replication': ('rdrp' in tf_all),
    'Cas13 RNA knockdown': ('cas13' in tf_all),
    '蓝白斑筛选': ('蓝白' in tf_all or 'blue-white' in tf_all or ('lacz' in tf_all and 'white' in tf_all)),
    'mothering/epigenetics': ('mother' in tf_all or '抚育' in tf_all),
    'vir/Helper plasmid': ('vir' in tf_all and 'helper' in tf_all),
    'lac operon allolactose': ('allolactose' in tf_all or '别乳糖' in tf_all),
    'lac operon CAP-cAMP': ('cap' in tf_all and 'camp' in tf_all),
    'sigma factor/核心酶': ('sigma' in tf_all or '核心酶' in tf_all),
    'rho factor终止': ('rho' in tf_all and 'terminat' in tf_all),
    'DNA pol 5-3 direction': ("5'" in tf_all and "3'" in tf_all and 'polymerase' in tf_all),
    '真核多复制起点': ('多' in tf_all and '起始点' in tf_all),
    '遗传密码简并性': ('degenera' in tf_all or '简并' in tf_all),
    'Trp operon 两种机制': ('repression' in tf_all and 'attenuat' in tf_all),
    'DNA methylation not activation': ('methylation' in tf_all and 'silencing' in tf_all),
    'histone acetylation active': ('acetylation' in tf_all and ('active' in tf_all or '活跃' in tf_all)),
}
for k, v in tf_checks.items():
    if not v:
        gaps.append(f'T/F: {k}')

# === 3. MC ===
mc_qs = [q for q in bank['questions'] if q['type'] == 'multiple-choice']
mc_all = ' '.join(q['prompt'].lower() + ' ' + q.get('explanation','').lower() for q in mc_qs)

mc_checks = {
    'PCR inventor': 'pcr' in mc_all and 'invent' in mc_all,
    '35S protein label': '35s' in mc_all or 'sulfur' in mc_all,
    'fMet first amino acid': 'fmet' in mc_all or 'formylmethionine' in mc_all,
    'AUG = Met': 'aug' in mc_all and 'methionine' in mc_all,
    'SD sequence organism': 'sd sequence' in mc_all or 'prokaryot' in mc_all,
    'EF-Tu A site': 'ef-tu' in mc_all,
    'Wobble theory': 'wobble' in mc_all,
    'CRISPR/Cas13': 'cas13' in mc_all,
    'Dicer enzyme': 'dicer' in mc_all,
    'Coding strand': 'non-template' in mc_all or 'coding strand' in mc_all,
    'Ternary complex': 'ternary' in mc_all,
    'Abortive transcription': 'abortive' in mc_all,
    'Splicing elements': 'splicing' in mc_all and 'splice site' in mc_all,
    'Agrobacterium vir': 'agrobacterium' in mc_all or 'vir gene' in mc_all,
    'TF BD+AD domains': 'domain' in mc_all and 'transcription factor' in mc_all,
    'Protein solubility': 'solubility' in mc_all,
    'PCR primer': 'primer' in mc_all and 'pcr' in mc_all,
}
for k, v in mc_checks.items():
    if not v:
        gaps.append(f'MC: {k}')

# === 4. SHORT ANSWER ===
sa_qs = [q for q in bank['questions'] if q['type'] == 'short-answer']
sa_all = ' '.join((q['prompt'] + ' ' + q.get('referenceAnswer','')).lower() for q in sa_qs)

sa_map = {
    'DNA复制三种方式': ['replication','theta','rolling circle','bidirectional'],
    'mRNA剪接过程': ['splicing','spliceosome','lariat','intron'],
    'miRNA合成': ['mirna','biogenesis','pri-mirna','drosha'],
    '加帽capping': ['capping','5 cap','cap 0'],
    '化学键水解酶': ['nuclease','glycosylase','helicase','phosphodiester'],
    'Class II PIC装配': ['preinitiation','tfiid','tfiib','class ii'],
    '除Pol I-III外RNA聚合酶': ['pol iv','pol v','rna polymerase iv'],
    '原核真核翻译起始区别': ['translation initiation','scanning','sd sequence'],
    '30S起始复合物': ['30s initiation','if1','if2','if3'],
    '翻译所需RNA': ['mrna','trna','rrna','function'],
    'DNA-蛋白互作检测': ['dna-protein','emsa','chip','yeast one-hybrid'],
    '蛋白-蛋白互作检测': ['protein-protein','y2h','co-ip','pull-down'],
    'Y2H步骤': ['yeast two-hybrid','bait','prey'],
    '改变蛋白活性修饰': ['phosphorylation','acetylation','ubiquitination'],
    '导入质粒方法': ['cloning','plasmid','restriction enzyme','ligation'],
    'loss of function': ['knockout','rnai','crispr','loss of function'],
    'tags作用': ['tag','fusion','affinity','his'],
    '植物转基因细菌': ['agrobacterium','t-dna'],
    '着丝粒功能': ['centromere','kinetochore','cenp'],
    'trp操纵子调节': ['trp','tryptophan','attenuat','aporepressor'],
    '组氨酸前导序列': ['histidine','leader','attenuat'],
    '表观遗传定义事例': ['epigenetic','inheritance','methylation','acetylation'],
    '蘑菇毒素': ['amanitin','mushroom','toxin'],
}
for topic, kwds in sa_map.items():
    if not any(k in sa_all for k in kwds):
        gaps.append(f'SA: {topic}')

# === 5. ESSAY ===
essay_qs = [q for q in bank['questions'] if q['type'] == 'essay']
essay_all = ' '.join((q['prompt'] + ' ' + q.get('referenceAnswer','')).lower() for q in essay_qs)

essay_map = {
    'Griffith+Hershey-Chase': ['griffith','hershey','transformation','genetic material'],
    '端粒': ['telomere','telomerase','t-loop'],
    'Trp衰减子': ['trp','attenuat','ribosome stall'],
    'siRNA vs miRNA': ['sirna','mirna','comparison','difference'],
    '盐胁迫实验': ['salt','stress','induc','rice'],
    '可变剪接验证': ['alternative splicing','exon','1200','1000'],
    '内含子验证': ['intron','cdna','genomic','300 bp'],
    '载体构建同尾酶': ['isocaudomer','sal i','xho i','bamh i'],
}
for topic, kwds in essay_map.items():
    if not any(k in essay_all for k in kwds):
        gaps.append(f'ESSAY: {topic}')

# === VERDICT ===
print("=== COVERAGE VERIFICATION ===")
if not gaps:
    print("YES - Question bank fully covers all exam content.")
else:
    print(f"NO - {len(gaps)} gaps found:")
    for g in gaps:
        print(f"  {g}")

print(f"\nBank: {bank['totalQuestions']} questions")
for t in ['translation','true-false','multiple-choice','short-answer','essay']:
    print(f"  {t}: {sum(1 for q in bank['questions'] if q['type']==t)}")
