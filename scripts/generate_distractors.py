"""Generate plausible distractors for all 17 multiple-choice questions."""

import json

with open('public/question-bank.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

distractors = {
    'multiple-choice-1-q-001': {
        'answerKey': 'C',
        'answerText': 'Kary Mullis（凯利·穆利斯）',
        'options': [
            {'key': 'A', 'text': 'Frederick Sanger（弗雷德里克·桑格）'},
            {'key': 'B', 'text': 'Walter Gilbert（沃尔特·吉尔伯特）'},
            {'key': 'C', 'text': 'Kary Mullis（凯利·穆利斯）'},
            {'key': 'D', 'text': 'Hamilton Smith（汉密尔顿·史密斯）'},
        ],
    },
    'multiple-choice-1-q-002': {
        'answerKey': 'B',
        'answerText': '³⁵S（硫-35）',
        'options': [
            {'key': 'A', 'text': '³²P（磷-32）'},
            {'key': 'B', 'text': '³⁵S（硫-35）'},
            {'key': 'C', 'text': '¹⁴C（碳-14）'},
            {'key': 'D', 'text': '³H（氚/氢-3）'},
        ],
    },
    'multiple-choice-2-q-003': {
        'answerKey': 'B',
        'answerText': 'N-甲酰甲硫氨酸（fMet）',
        'options': [
            {'key': 'A', 'text': '甲硫氨酸（Met）'},
            {'key': 'B', 'text': 'N-甲酰甲硫氨酸（fMet）'},
            {'key': 'C', 'text': '脯氨酸（Pro）'},
            {'key': 'D', 'text': '甘氨酸（Gly）'},
        ],
    },
    'multiple-choice-2-q-004': {
        'answerKey': 'A',
        'answerText': '甲硫氨酸（Met）；原核起始为fMet，延伸及真核均为Met',
        'options': [
            {'key': 'A', 'text': '甲硫氨酸（Met）'},
            {'key': 'B', 'text': '色氨酸（Trp）'},
            {'key': 'C', 'text': '苯丙氨酸（Phe）'},
            {'key': 'D', 'text': '亮氨酸（Leu）'},
        ],
    },
    'multiple-choice-2-q-005': {
        'answerKey': 'A',
        'answerText': '原核生物（细菌、古菌）',
        'options': [
            {'key': 'A', 'text': '原核生物（细菌、古菌）'},
            {'key': 'B', 'text': '真核生物'},
            {'key': 'C', 'text': '所有生物'},
            {'key': 'D', 'text': '仅病毒'},
        ],
    },
    'multiple-choice-2-q-006': {
        'answerKey': 'A',
        'answerText': 'EF-Tu（延伸因子Tu）',
        'options': [
            {'key': 'A', 'text': 'EF-Tu（延伸因子Tu）'},
            {'key': 'B', 'text': 'EF-G（延伸因子G）'},
            {'key': 'C', 'text': 'EF-Ts（延伸因子Ts）'},
            {'key': 'D', 'text': 'IF2（起始因子2）'},
        ],
    },
    'multiple-choice-2-q-007': {
        'answerKey': 'A',
        'answerText': "tRNA反密码子5'端第一位碱基与mRNA密码子3'端第三位碱基可发生非标准配对（摆动配对），使一种tRNA可识别多个同义密码子",
        'options': [
            {'key': 'A', 'text': "tRNA反密码子5'端碱基与mRNA密码子3'端第三位发生非标准配对"},
            {'key': 'B', 'text': "mRNA密码子5'端碱基与tRNA反密码子3'端发生非标准配对"},
            {'key': 'C', 'text': '核糖体在翻译延伸过程中催化密码子-反密码子间的摆动'},
            {'key': 'D', 'text': '氨基酰-tRNA合成酶可识别多种tRNA并催化非标准氨基酸装载'},
        ],
    },
    'multiple-choice-3-q-008': {
        'answerKey': 'A',
        'answerText': '靶向切割RNA，实现RNA敲低',
        'options': [
            {'key': 'A', 'text': '靶向切割RNA，实现RNA敲低'},
            {'key': 'B', 'text': '靶向切割DNA，实现基因敲除'},
            {'key': 'C', 'text': '靶向降解蛋白质，实现蛋白敲低'},
            {'key': 'D', 'text': '催化RNA脱氨基编辑'},
        ],
    },
    'multiple-choice-3-q-009': {
        'answerKey': 'C',
        'answerText': 'Dicer',
        'options': [
            {'key': 'A', 'text': 'Drosha'},
            {'key': 'B', 'text': 'Exportin-5'},
            {'key': 'C', 'text': 'Dicer'},
            {'key': 'D', 'text': 'RISC'},
        ],
    },
    'multiple-choice-3-q-010': {
        'answerKey': 'A',
        'answerText': '非模板链（non-template strand）',
        'options': [
            {'key': 'A', 'text': '非模板链（non-template strand）'},
            {'key': 'B', 'text': '模板链（template strand）'},
            {'key': 'C', 'text': '反义链（antisense strand）'},
            {'key': 'D', 'text': '后随链（lagging strand）'},
        ],
    },
    'multiple-choice-3-q-011': {
        'answerKey': 'A',
        'answerText': '核心RNA聚合酶 + DNA模板链 + 新生RNA链',
        'options': [
            {'key': 'A', 'text': '核心RNA聚合酶 + DNA模板链 + 新生RNA链'},
            {'key': 'B', 'text': '核心RNA聚合酶 + σ因子 + DNA模板链'},
            {'key': 'C', 'text': '全酶（holoenzyme）+ DNA模板链 + 新生RNA链'},
            {'key': 'D', 'text': 'RNA聚合酶 + 核糖体 + mRNA'},
        ],
    },
    'multiple-choice-3-q-012': {
        'answerKey': 'A',
        'answerText': 'RNA聚合酶频繁发生流产转录（abortive transcription），长基因需要多次重启起始',
        'options': [
            {'key': 'A', 'text': 'RNA聚合酶频繁发生流产转录，长基因需要多次重启'},
            {'key': 'B', 'text': 'RNA聚合酶的延伸速度极慢且无法调控'},
            {'key': 'C', 'text': '长mRNA在转录完成前即被核酸酶降解'},
            {'key': 'D', 'text': '内含子必须在转录完成前完成剪接'},
        ],
    },
    'multiple-choice-3-q-013': {
        'answerKey': 'A',
        'answerText': "5'剪接位点（GU）+ 3'剪接位点（AG）+ 分支点序列（branch point）",
        'options': [
            {'key': 'A', 'text': "5'剪接位点 + 3'剪接位点 + 分支点序列"},
            {'key': 'B', 'text': "5'帽子 + 3'polyA尾 + 分支点序列"},
            {'key': 'C', 'text': "5'剪接位点 + 3'剪接位点 + TATA框"},
            {'key': 'D', 'text': "外显子 + 内含子 + 5'剪接位点"},
        ],
    },
    'multiple-choice-4-q-014': {
        'answerKey': 'A',
        'answerText': 'vir（毒性）基因',
        'options': [
            {'key': 'A', 'text': 'vir（毒性）基因'},
            {'key': 'B', 'text': 'T-DNA基因'},
            {'key': 'C', 'text': '抗生素抗性基因'},
            {'key': 'D', 'text': 'ori（复制起点）'},
        ],
    },
    'multiple-choice-5-q-015': {
        'answerKey': 'A',
        'answerText': 'DNA结合结构域（BD）+ 转录激活结构域（AD）',
        'options': [
            {'key': 'A', 'text': 'DNA结合结构域（BD）+ 转录激活结构域（AD）'},
            {'key': 'B', 'text': '二聚化结构域 + 核定位信号（NLS）'},
            {'key': 'C', 'text': '配体结合结构域 + DNA结合结构域'},
            {'key': 'D', 'text': '抑制结构域 + 染色质重塑结构域'},
        ],
    },
    'multiple-choice-5-q-016': {
        'answerKey': 'B',
        'answerText': '同时合成多种蛋白——竞争分子伴侣资源，加剧折叠错误',
        'options': [
            {'key': 'A', 'text': '降低诱导温度（如从37°C降至18–25°C）'},
            {'key': 'B', 'text': '同时共表达多种重组蛋白'},
            {'key': 'C', 'text': '使用融合标签（如MBP、GST、Trx）'},
            {'key': 'D', 'text': '共表达分子伴侣（如GroEL/GroES）'},
        ],
    },
    'multiple-choice-5-q-017': {
        'answerKey': 'A',
        'answerText': "下游引物与模板链3'端反向互补，5'→3'延伸方向与上游引物相向",
        'options': [
            {'key': 'A', 'text': "与模板链3'端反向互补，延伸方向与上游引物相向"},
            {'key': 'B', 'text': "与模板链5'端序列完全相同"},
            {'key': 'C', 'text': '与上游引物序列反向互补'},
            {'key': 'D', 'text': '与上游引物序列完全相同'},
        ],
    },
}

# Apply distractors
for q in data['questions']:
    if q['type'] == 'multiple-choice' and q['id'] in distractors:
        d = distractors[q['id']]
        q['options'] = d['options']
        q['answerKey'] = d['answerKey']
        q['answerText'] = d['answerText']
        q['distractorsGenerated'] = True

with open('public/question-bank.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Verify
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

mc_qs = [q for q in data['questions'] if q['type'] == 'multiple-choice']
all_good = True
for q in mc_qs:
    has_opts = len(q.get('options', [])) == 4
    has_key = q.get('answerKey') in ('A', 'B', 'C', 'D')
    status = 'OK' if (has_opts and has_key) else 'XX'
    if not (has_opts and has_key):
        all_good = False
    print(f"{status} {q['id']}: key={q.get('answerKey')} opts={len(q.get('options', []))}")

print(f"\nTotal MC with distractors: {sum(1 for q in mc_qs if q.get('distractorsGenerated'))} / {len(mc_qs)}")
print("All OK!" if all_good else "SOME ISSUES!")
