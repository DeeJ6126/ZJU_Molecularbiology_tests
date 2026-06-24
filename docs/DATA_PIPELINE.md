# Data Pipeline

The question bank originates from `data/分子生物学历年卷.docx`, a single DOCX containing ~205 questions across 5 types.

## Pipeline scripts (run in order)

### 1. `scripts/parse_docx_to_bank.py`

Parses the DOCX into `public/question-bank.json`.

- **Tables 0-6**: Translation terms (7 subcategories, 104 total)
  - 2-column tables: `col[0]=English, col[1]=Chinese`
  - 3-column tables: `col[0]=English, col[2]=Chinese` (col[1] is duplicate English)
  - Abbreviation handling: `parse_abbreviation()` extracts `"ChIP (Chromatin immunoprecipitation)"` → `abbr="ChIP", full="Chromatin immunoprecipitation"`
  - Bare abbreviations: `ABBREVIATION_FULL_FORMS` dict maps `mRNA→messenger RNA`, `PCR→polymerase chain reaction`, etc. (~50 entries)
- **Paragraphs 10-55**: True/false questions. Pattern: statement → `结论：正确/错误` → `解析：...`
- **Paragraphs 56-115**: Multiple choice. Pattern: question → `答案：X` → `解析：...`
- **Paragraphs 116-215**: Short answer. Uses `_is_likely_question_title()` heuristic (first-line analysis)
- **Paragraphs 216-247**: Essay questions (first 4 subcategories, truncates before supplementary material)

Dependency: `python-docx`

### 2. `scripts/translate_prompts.py`

After `parse_docx_to_bank.py`, all non-translation questions have Chinese prompts/explanations/answers.
This script applies English translations via a hardcoded mapping dict (question ID → English text).

- Skips `type: "translation"` questions (must stay Chinese)
- Translates: `prompt`, `explanation`, `referenceAnswer` for all other types

### 3. `scripts/generate_distractors.py`

**DONE.** Generates A/B/C/D distractors for all 17 multiple-choice questions.
Hardcoded domain-plausible distractors (same-pathway enzymes, common misconceptions, etc.).
No API key required — edit the script directly to update options.

Options are **English-only**; `explanation` stays in Chinese from the DOCX parser.

## ⚠️ Critical: Regeneration order

`parse_docx_to_bank.py` ALWAYS regenerates the JSON from scratch using the Chinese DOCX.
This **overwrites** English translations AND distractors. After any parser change:

```bash
python scripts/parse_docx_to_bank.py   # Regenerate from DOCX
python scripts/translate_prompts.py    # Re-apply English translations
python scripts/generate_distractors.py # Re-generate MC options
```

## Question ID format

```
{type-prefix}-{subcategory}-q-{number:03d}

Examples:
  translation-1-q-001       # Translation, subcat 1 (基础分子生物学概念), Q1
  true-false-3-q-007        # True/false, subcat 3 (转录与RNA生物学), Q7
  multiple-choice-2-q-005   # MC, subcat 2 (翻译过程与机制), Q5
  short-answer-8-q-042      # Short answer, subcat 8 (分子生物学实验技术), Q42
  essay-1-q-001             # Essay, subcat 1 (RNA加工与可变剪接), Q1
```

## Category structure

Categories are nested: `parentTitle` (question type name) + `title` (subcategory name).

```
中英名词互译
  ├── 基础分子生物学概念 (30 Qs)
  ├── 核酸结构与功能 (34 Qs)
  ├── 蛋白质结构与修饰 (14 Qs)
  └── ... (7 subcategories total)

判断题
  ├── 遗传密码与翻译 (5 Qs)
  ├── DNA复制与修复 (1 Q)
  └── ... (5 subcategories total)

选择题 (6 subcategories)
简答题 (10 subcategories)  
分析论述题 (4 subcategories)
```
