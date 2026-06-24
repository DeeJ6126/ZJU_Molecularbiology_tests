"""Generate plausible distractors for all 17 multiple-choice questions."""

import json

with open('public/question-bank.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

distractors = {
    'multiple-choice-1-q-001': {
        'answerKey': 'C',
        'answerText': 'Kary Mullis',
        'options': [
            {'key': 'A', 'text': 'Frederick Sanger'},
            {'key': 'B', 'text': 'Walter Gilbert'},
            {'key': 'C', 'text': 'Kary Mullis'},
            {'key': 'D', 'text': 'Hamilton Smith'},
        ],
    },
    'multiple-choice-1-q-002': {
        'answerKey': 'B',
        'answerText': '³⁵S',
        'options': [
            {'key': 'A', 'text': '³²P'},
            {'key': 'B', 'text': '³⁵S'},
            {'key': 'C', 'text': '¹⁴C'},
            {'key': 'D', 'text': '³H'},
        ],
    },
    'multiple-choice-2-q-003': {
        'answerKey': 'B',
        'answerText': 'N-formylmethionine (fMet)',
        'options': [
            {'key': 'A', 'text': 'Methionine (Met)'},
            {'key': 'B', 'text': 'N-formylmethionine (fMet)'},
            {'key': 'C', 'text': 'Proline (Pro)'},
            {'key': 'D', 'text': 'Glycine (Gly)'},
        ],
    },
    'multiple-choice-2-q-004': {
        'answerKey': 'A',
        'answerText': 'Methionine (Met); fMet in prokaryotic initiation, Met in elongation and eukaryotes',
        'options': [
            {'key': 'A', 'text': 'Methionine (Met)'},
            {'key': 'B', 'text': 'Tryptophan (Trp)'},
            {'key': 'C', 'text': 'Phenylalanine (Phe)'},
            {'key': 'D', 'text': 'Leucine (Leu)'},
        ],
    },
    'multiple-choice-2-q-005': {
        'answerKey': 'A',
        'answerText': 'Prokaryotes (bacteria and archaea)',
        'options': [
            {'key': 'A', 'text': 'Prokaryotes (bacteria and archaea)'},
            {'key': 'B', 'text': 'Eukaryotes'},
            {'key': 'C', 'text': 'All organisms'},
            {'key': 'D', 'text': 'Viruses only'},
        ],
    },
    'multiple-choice-2-q-006': {
        'answerKey': 'A',
        'answerText': 'EF-Tu (Elongation Factor Tu)',
        'options': [
            {'key': 'A', 'text': 'EF-Tu (Elongation Factor Tu)'},
            {'key': 'B', 'text': 'EF-G (Elongation Factor G)'},
            {'key': 'C', 'text': 'EF-Ts (Elongation Factor Ts)'},
            {'key': 'D', 'text': 'IF2 (Initiation Factor 2)'},
        ],
    },
    'multiple-choice-2-q-007': {
        'answerKey': 'A',
        'answerText': 'The 5\' base of the tRNA anticodon can form non-canonical (wobble) pairs with the 3\' third base of the mRNA codon, allowing one tRNA to recognize multiple synonymous codons',
        'options': [
            {'key': 'A', 'text': 'The 5\' base of tRNA anticodon wobble-pairs with the 3\' third base of mRNA codon'},
            {'key': 'B', 'text': 'The 5\' base of mRNA codon wobble-pairs with the 3\' base of tRNA anticodon'},
            {'key': 'C', 'text': 'The ribosome catalyzes wobble movement during translocation'},
            {'key': 'D', 'text': 'Aminoacyl-tRNA synthetase recognizes multiple tRNAs via wobble pairing'},
        ],
    },
    'multiple-choice-3-q-008': {
        'answerKey': 'A',
        'answerText': 'Targets and cleaves RNA, achieving RNA knockdown',
        'options': [
            {'key': 'A', 'text': 'Targets and cleaves RNA, achieving RNA knockdown'},
            {'key': 'B', 'text': 'Targets and cleaves DNA, achieving gene knockout'},
            {'key': 'C', 'text': 'Targets and degrades proteins, achieving protein knockdown'},
            {'key': 'D', 'text': 'Catalyzes RNA deamination editing'},
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
        'answerText': 'Non-template strand (coding strand / sense strand)',
        'options': [
            {'key': 'A', 'text': 'Non-template strand (coding / sense strand)'},
            {'key': 'B', 'text': 'Template strand (non-coding / antisense strand)'},
            {'key': 'C', 'text': 'Antisense strand'},
            {'key': 'D', 'text': 'Lagging strand'},
        ],
    },
    'multiple-choice-3-q-011': {
        'answerKey': 'A',
        'answerText': 'Core RNA polymerase + DNA template strand + nascent RNA',
        'options': [
            {'key': 'A', 'text': 'Core RNA polymerase + DNA template strand + nascent RNA'},
            {'key': 'B', 'text': 'Core RNA polymerase + sigma factor + DNA template strand'},
            {'key': 'C', 'text': 'Holoenzyme + DNA template strand + nascent RNA'},
            {'key': 'D', 'text': 'RNA polymerase + ribosome + mRNA'},
        ],
    },
    'multiple-choice-3-q-012': {
        'answerKey': 'A',
        'answerText': 'RNA polymerase frequently undergoes abortive transcription, requiring multiple re-initiation attempts for long genes',
        'options': [
            {'key': 'A', 'text': 'RNA polymerase frequently undergoes abortive transcription, requiring multiple re-initiation attempts'},
            {'key': 'B', 'text': 'RNA polymerase elongation rate is extremely slow and cannot be regulated'},
            {'key': 'C', 'text': 'Long mRNAs are degraded by nucleases before transcription completes'},
            {'key': 'D', 'text': 'Introns must be spliced before transcription can finish'},
        ],
    },
    'multiple-choice-3-q-013': {
        'answerKey': 'A',
        'answerText': "5' splice site (GU) + 3' splice site (AG) + branch point sequence (A residue)",
        'options': [
            {'key': 'A', 'text': "5' splice site (GU) + 3' splice site (AG) + branch point (A)"},
            {'key': 'B', 'text': "5' cap + 3' polyA tail + branch point"},
            {'key': 'C', 'text': "5' splice site + 3' splice site + TATA box"},
            {'key': 'D', 'text': 'Exon + intron + 5\' splice site'},
        ],
    },
    'multiple-choice-4-q-014': {
        'answerKey': 'A',
        'answerText': 'vir (virulence) genes',
        'options': [
            {'key': 'A', 'text': 'vir (virulence) genes'},
            {'key': 'B', 'text': 'T-DNA genes'},
            {'key': 'C', 'text': 'Antibiotic resistance genes'},
            {'key': 'D', 'text': 'ori (origin of replication)'},
        ],
    },
    'multiple-choice-5-q-015': {
        'answerKey': 'A',
        'answerText': 'DNA-binding domain (BD) + transcription activation domain (AD)',
        'options': [
            {'key': 'A', 'text': 'DNA-binding domain (BD) + transcription activation domain (AD)'},
            {'key': 'B', 'text': 'Dimerization domain + nuclear localization signal (NLS)'},
            {'key': 'C', 'text': 'Ligand-binding domain + DNA-binding domain'},
            {'key': 'D', 'text': 'Repression domain + chromatin remodeling domain'},
        ],
    },
    'multiple-choice-5-q-016': {
        'answerKey': 'B',
        'answerText': 'Co-expressing multiple recombinant proteins simultaneously — competes for chaperone resources, worsening misfolding',
        'options': [
            {'key': 'A', 'text': 'Lowering induction temperature (e.g., from 37°C to 18–25°C)'},
            {'key': 'B', 'text': 'Co-expressing multiple recombinant proteins simultaneously'},
            {'key': 'C', 'text': 'Using fusion tags (e.g., MBP, GST, Trx)'},
            {'key': 'D', 'text': 'Co-expressing molecular chaperones (e.g., GroEL/GroES)'},
        ],
    },
    'multiple-choice-5-q-017': {
        'answerKey': 'A',
        'answerText': "The downstream primer must be reverse-complementary to the template strand's 3' end, with its 5'→3' extension direction facing the upstream primer",
        'options': [
            {'key': 'A', 'text': "Reverse-complementary to the template 3' end, extending toward the upstream primer"},
            {'key': 'B', 'text': "Identical to the template 5' end sequence"},
            {'key': 'C', 'text': 'Reverse-complementary to the upstream primer sequence'},
            {'key': 'D', 'text': 'Identical to the upstream primer sequence'},
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
