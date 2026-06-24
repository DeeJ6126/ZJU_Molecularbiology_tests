#!/usr/bin/env python
"""Build data/分子生物学历年客观题.md from agent outputs."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read Agent C's MC output
with open('data/历年卷/选择题汇总.md', 'r', encoding='utf-8') as f:
    mc_text = f.read()

out = []
out.append('# 分子生物学历年客观题汇编')
out.append('')
out.append('> 来源：`data/历年卷/`（21春夏、21秋冬、22春夏、23春夏）')
out.append('> 题型：中英名词互译 · 判断题 · 选择题')
out.append('> 答案来源：`data/课件/`（课程PPT）')
out.append('')
out.append('---')
out.append('')

# === Part 1: Translation ===
out.append('# 一、中英名词互译（55题）')
out.append('')
out.append('## 英译中（26题）')
out.append('')

en_to_cn = [
    ("alternative splicing", "可变剪接"),
    ("attenuator", "衰减子"),
    ("autoradiography", "放射自显影"),
    ("C value paradox", "C值悖论"),
    ("centromere", "着丝粒"),
    ("codon preference / codon bias", "密码子偏好性"),
    ("deoxyribonucleic acid", "脱氧核糖核酸"),
    ("enhancer", "增强子"),
    ("epigenetics", "表观遗传学"),
    ("eucaryon / eukaryote", "真核生物"),
    ("gel electrophoresis", "凝胶电泳"),
    ("kinetochore", "动粒/着丝点"),
    ("lncRNA (long non-coding RNA)", "长链非编码RNA"),
    ("meiosis", "减数分裂"),
    ("methylation", "甲基化"),
    ("mitosis", "有丝分裂"),
    ("nucleoid", "拟核"),
    ("nucleosome", "核小体"),
    ("phosphorylation", "磷酸化"),
    ("snRNPs / snRNP", "核小核糖核蛋白颗粒"),
    ("spliceosome", "剪接体"),
    ("trans-activation domain", "反式激活结构域"),
    ("transforming factor", "转化因子"),
    ("transposon", "转座子"),
    ("trans-splicing", "反式剪接"),
    ("ubiquitination", "泛素化"),
]
for en, cn in en_to_cn:
    out.append(f"- **{en}** → {cn}")
out.append('')

out.append('## 中译英（29题）')
out.append('')
cn_to_en = [
    ("氨基酸", "amino acid"),
    ("表观遗传 / 表观遗传学", "epigenetics"),
    ("表观遗传组学", "epigenomics"),
    ("操纵区 / 操纵位点", "operator"),
    ("操纵元 / 操纵子", "operon"),
    ("蛋白质组学 / 蛋白组学", "proteomics"),
    ("多顺反子", "polycistron"),
    ("翻译", "translation"),
    ("复制滑移", "replication slippage / slipped strand mispairing"),
    ("功能基因组学", "functional genomics"),
    ("核苷酸", "nucleotide"),
    ("核小体", "nucleosome"),
    ("甲基化", "methylation"),
    ("解旋酶", "helicase"),
    ("开放阅读框", "open reading frame (ORF)"),
    ("拟核", "nucleoid"),
    ("噬菌体", "bacteriophage / phage"),
    ("噬菌体展示", "phage display"),
    ("糖基化", "glycosylation"),
    ("同源重组", "homologous recombination"),
    ("图位克隆", "map-based cloning"),
    ("异染色质", "heterochromatin"),
    ("荧光共振能量转移", "fluorescence resonance energy transfer (FRET)"),
    ("原位杂交", "in situ hybridization"),
    ("终止子", "terminator"),
    ("转录", "transcription"),
    ("转座子", "transposon"),
    ("组氨酸", "histidine"),
    ("组蛋白", "histone"),
]
for cn, en in cn_to_en:
    out.append(f"- **{cn}** → {en}")
out.append('')

# === Part 2: T/F ===
out.append('---')
out.append('')
out.append('# 二、判断题（20题）')
out.append('')

tf_qs = [
    ("遗传密码与翻译", [
        ("原核生物翻译起始使用甲酰甲硫氨酸（fMet-tRNA^fMet），而真核生物翻译起始使用甲硫氨酸（Met-tRNAi^Met）。", True,
         "MB13(7)第24页指出原核起始氨基酸为N-formyl-methionine (fMet)；第34页对比说明真核起始氨基酸为methionine (Met)，不含甲酰基。"),
        ("原核生物mRNA的5'UTR含有SD序列（Shine-Dalgarno sequence），与16S rRNA 3'端互补配对，帮助核糖体30S亚基定位起始密码子。", True,
         "MB13(7)第26-27页：SD序列为富含G的序列（consensus AGGAGGU），位于起始密码子上游约10nt处，与16S rRNA 3'端互补配对。"),
        ("真核生物翻译起始时，40S核糖体亚基识别mRNA 5'端帽子结构，然后沿mRNA向下游扫描，直至遇到第一个处于合适上下文中的AUG起始密码子。", True,
         "MB13(7)第35页：真核40S核糖体亚基通过结合5'-cap并向下游扫描找到第一个处于有利上下文中的AUG。最佳上下文为CCRCCAUGG。"),
        ("在原核生物中，IF3（起始因子3）的功能是促进fMet-tRNA与30S亚基的结合。", False,
         "MB13(7)第10页和第22页：IF3结合游离的30S亚基并阻止其与50S亚基重新结合，介导SD序列与16S rRNA的配对。促进fMet-tRNA结合的主要是IF2（需要GTP）。"),
        ("遗传密码具有简并性（degeneracy），意味着一个特定的密码子可以编码多种氨基酸。", False,
         "MB13(7)第46页：遗传密码是unambiguous（无歧义的），一个特定密码子只编码一种氨基酸；但它是degenerate（简并的），即多种密码子可以编码同一种氨基酸。"),
    ]),
    ("转录与RNA生物学", [
        ("真核生物Class III基因的通用转录因子中，TFIIIA是5S rRNA基因转录所必需的，但对tRNA基因的转录不是必需的。", True,
         "MB8第44页：TFIIIA is required for the synthesis of 5s rRNA, but not tRNA. TFIIIB and C are required by both."),
        ("原核生物中，RNA聚合酶核心酶（core enzyme，由α2ββ'组成）可以独立识别启动子并准确起始转录。", False,
         "MB7第10页：核心酶不能转录完整DNA，没有σ因子时丧失转录起始位点的特异性。"),
        ("Class III启动子全部位于基因内部（gene-internal），与Class II启动子位于基因上游不同。", False,
         "MB8第26-29页：Class III启动子分为两类——经典Class III启动子位于基因内部（如5S rRNA、tRNA）；非经典Class III启动子与Class II一样位于基因上游（如U6 snRNA）。"),
        ("siRNA（small interfering RNA）通过RISC介导同源mRNA的序列特异性切割和降解。", True,
         "MB12第13页和第31页：siRNA装载入RISC（含Argonaute蛋白），引导RISC识别并切割同源mRNA使其降解。"),
        ("ρ因子（Rho factor）是原核生物所有转录终止过程都必需的蛋白质因子。", False,
         "MB7第28-35页：原核转录终止有两种机制——ρ依赖性和ρ非依赖性。后者通过发夹结构+一串T残基即可终止，不需要ρ因子。"),
    ]),
    ("DNA复制与修复", [
        ("RNA依赖的RNA聚合酶（RdRp）参与原核生物DNA复制过程中的引物合成。", False,
         "MB12第14页：RdRp以RNA为模板合成RNA，不参与DNA复制。DNA复制中的RNA引物由引物酶（primase）合成（MB6第35页）。"),
        ("DNA聚合酶只能沿5'→3'方向合成新的DNA链，阅读模板链的方向为3'→5'。", True,
         "MB6第17页：All DNA polymerases synthesize DNA in the 5' to 3' direction, reading the template 3' to 5'."),
        ("真核生物染色体DNA复制只有一个复制起始点，从此起始点向两个方向进行双向复制。", False,
         "MB6第51页：真核生物染色体有多个复制起始点（多个replicon），原核生物染色体才只有一个起始点。"),
    ]),
    ("基因表达调控", [
        ("Trp操纵子中，辅阻遏蛋白（apo-repressor）在色氨酸浓度低时也能与操纵区结合，抑制结构基因的转录。", False,
         "MB7第52页：Aporepressor本身无活性，必须与色氨酸结合后才能作为活性阻遏蛋白结合操纵区。Low trp, no repression。"),
        ("Trp操纵子仅通过阻遏机制（repression）进行转录水平的调控。", False,
         "MB7第54页：Trp操纵子同时受阻遏（70倍）和衰减（attenuation，额外10倍）两种机制调控，总调控达700倍。"),
        ("乳糖操纵子中，别乳糖（allolactose）作为诱导物与lac阻遏蛋白结合，使阻遏蛋白从操纵区解离，从而开启操纵子转录。", True,
         "MB7第43页：Allolactose acts as an inducer by binding the repressor, repressor dissociates from the operator."),
        ("乳糖操纵子（lac operon）的调控中，当葡萄糖和乳糖同时存在时，lac操纵子高效表达。", False,
         "MB7第48页：lac操纵子的结构基因只有在葡萄糖不存在且乳糖存在时才表达。葡萄糖存在导致cAMP浓度低，CAP-cAMP复合物不能有效结合启动子（分解代谢物阻遏）。"),
    ]),
    ("表观遗传学", [
        ("大鼠的母性抚育行为（舔舐/梳理和弓背哺乳，LG-ABN）可以通过表观遗传机制影响雌性后代的抚育行为方式，从而在代际间延续。", True,
         "MB16(7)第54页：高LG-ABN mothering导致NGFI-A表达增加，进而GR启动子去甲基化、组蛋白乙酰化增加、GR表达升高。表观遗传标记在代际间延续。"),
        ("DNA甲基化通常发生在CpG二核苷酸的胞嘧啶上，启动子区域CpG岛的甲基化通常与基因转录激活相关。", False,
         "MB16(7)第41-44页：启动子CpG岛的甲基化通常导致基因沉默（gene silencing），而非激活。"),
        ("组蛋白乙酰化通常与转录活跃的染色质区域相关，而组蛋白去乙酰化通常与基因沉默相关。", True,
         "MB16(7)第32页：Generally, histone acetylation is associated with transcriptionally active genes. Deacetylation is associated with inactive genes."),
    ]),
    ("分子克隆与实验技术", [
        ("在农杆菌介导的植物遗传转化双元载体系统中，辅助质粒（helper plasmid）含有vir基因，负责编码T-DNA加工和转移所需的蛋白质。", True,
         "MB4第78页：Helper plasmid containing the vir genes."),
        ("Cas13家族蛋白是RNA靶向的CRISPR系统效应蛋白，可介导RNA敲降（RNA knockdown），用于抑制RNA病毒和调控基因表达。", True,
         "MB5第56页：Cas13 family proteins mediated RNA Knockdown, suppression of RNA viruses."),
        ("蓝白斑筛选实验中，在含有IPTG和X-gal的培养基上，成功插入了外源DNA片段（使lacZ失活）的重组细菌菌落呈蓝色。", False,
         "蓝白斑筛选原理：外源DNA插入lacZ基因使其失活→不能产生β-半乳糖苷酶→无法分解X-gal→菌落呈白色。蓝色表示未插入外源片段（载体自连）。"),
    ]),
]

for cat_title, qs in tf_qs:
    out.append(f"## {cat_title}（{len(qs)}题）")
    out.append('')
    for stmt, is_true, explanation in qs:
        answer = "**正确**" if is_true else "**错误**"
        out.append(f"- 陈述：{stmt}")
        out.append(f"  - 答案：{answer}")
        out.append(f"  - 解析：{explanation}")
    out.append('')

# === Part 3: MC from Agent C ===
out.append('---')
out.append('')
out.append('# 三、选择题')
out.append('')

mc_lines = mc_text.split('\n')
in_mc = False
for line in mc_lines:
    s = line.strip()
    if s.startswith('# 三、'):
        continue
    if s.startswith('> '):
        continue
    if s.startswith('## '):
        in_mc = True
    if in_mc:
        s_clean = s.replace('**【已入库】** ', '').replace('**【新补】** ', '')
        out.append(s_clean)

result = '\n'.join(out)

with open('data/分子生物学历年客观题.md', 'w', encoding='utf-8') as f:
    f.write(result)

print(f"Written: {len(result)} chars, {len(result.splitlines())} lines")
print("Done!")
