# 分子生物学习题库 (Molecular Biology Exam Platform)

ZJU 分子生物学课程刷题工具。React 19 + Vite 8 + TypeScript 6，纯静态前端，localStorage 持久化。

## Quick start

```bash
npm install
npm run dev          # http://localhost:5173
npm run build        # dist/
```

## Project structure

```
data/
  分子生物学历年卷.docx    # Raw source (all questions)
  分子生物学历年卷.pdf     # Same content, PDF format
public/
  question-bank.json        # Generated: 213 questions, all types
scripts/
  parse_docx_to_bank.py          # DOCX → question-bank.json
  generate_distractors.py           # MC distractor generation (DONE)
  translate_prompts.py            # Chinese→English translation dict (non-translation Qs)
src/
  types.ts                  # All TypeScript interfaces
  main.tsx                  # Entry: BrowserRouter + App
  App.tsx                   # Routes + PracticeProvider wrapper
  App.css                   # All component styles
  index.css                 # CSS variables, base reset, responsive utilities
  context/
    practiceContextObject.ts # Context type definition
    PracticeContext.tsx      # Central state: session, mistakes, vocabulary, localStorage
  hooks/
    usePractice.ts           # Context accessor (throws if outside provider)
    useQuestionBank.ts       # fetch() question-bank.json with loading/error/reload
  lib/
    practice.ts              # Session creation, scoring, translation matching, shuffle
    categoryScope.ts         # Category/type filtering helpers
    vocabulary.ts            # English term tokenization, CRUD, import/export
    vocabulary.test.ts       # Node test runner tests
  components/
    AppLayout.tsx            # Top nav bar + <Outlet>
    TranslationInput.tsx     # Text input with abbreviation/singular-plural matching
    TrueFalseInput.tsx       # Two-button 正确/错误
    MultipleChoiceInput.tsx  # A/B/C/D option grid
    ShortAnswerInput.tsx     # Textarea + reveal answer + self-judge
    EssayInput.tsx           # Same pattern, larger textarea
    FlashcardReview.tsx      # Chinese term on card, Enter reveals English, Space speaks
    VocabularyPicker.tsx     # Click-to-collect English terms
  pages/
    IntroPage.tsx            # Landing: stats, feature cards, quick links
    CategorySelectionPage.tsx # Select question types & subcategories, start practice/review
    PracticePage.tsx         # Dispatches to correct question-type component
    ReviewPage.tsx           # Flashcard review wrapper
    ResultsPage.tsx          # Score breakdown, per-type stats
    MistakesPage.tsx         # Mistake list, start drill
    VocabularyPage.tsx       # Vocab list, status filters, import/export
    AboutPage.tsx            # Info about the app
```

## Question types (213 total, 109 non-translation + 104 translation)

| Type             | Count | Answer format                              |
|------------------|-------|--------------------------------------------|
| `translation`    | 104   | Text input (zh→en), abbreviation tolerant  |
| `true-false`     | 13    | Two buttons (正确/错误)                    |
| `multiple-choice`| 17    | A/B/C/D grid (distractors NOT yet generated)|
| `short-answer`   | 61    | Textarea + reveal answer + self-judge      |
| `essay`          | 18    | Same as short-answer, larger               |

## Translation matching rules

1. **Case-insensitive** exact match against `acceptableAnswers[]`
2. **Singular/plural tolerant**: `Prokaryote` matches `Prokaryotes` (cross-checked stems)
3. **Abbreviation required**: must type full term (e.g. `messenger RNA`), `mRNA` alone rejected
4. **Combined form accepted**: `mRNA (messenger RNA)` is valid
5. Abbreviation→full-term mapping in `parse_docx_to_bank.py` → `ABBREVIATION_FULL_FORMS` dict

## State management

`PracticeContext` owns everything, persisted to localStorage:
- `session` — current practice session (question order, answers, index)
- `selectedCategoryIds` — which categories user picked
- `mistakeRecords` — wrong answers + self-judged-as-wrong
- `vocabularyRecords` — English terms collected via picker

LocalStorage keys: `molecular-biology-{session,selection,mistakes,vocabulary}`

## Data pipeline (critical)

**Always run scripts in this order after editing the DOCX or parser:**

```bash
# 1. Parse DOCX → JSON (regenerates ALL questions from Chinese source)
python scripts/parse_docx_to_bank.py

# 2. Translate non-translation questions to English
python scripts/translate_prompts.py

# 3. Generate distractors for multiple-choice
python scripts/generate_distractors.py
```

⚠️ **WARNING**: `parse_docx_to_bank.py` regenerates the entire JSON from the Chinese DOCX.
This overwrites English translations AND distractors. You MUST re-run `translate_prompts.py`
and `generate_distractors.py` after it.

## Known limitations

1. **Multiple-choice distractors generated**. 17 MC questions now have English-only A/B/C/D options with domain-plausible distractors. Run `generate_distractors.py` to regenerate if questions change.
2. **Short-answer parsing includes answer fragments as questions** (~61 items, some are answer-paragraphs misidentified as questions). Manually review `short-answer-3-q-015` through `short-answer-10-q-061`.
3. **Essay section includes sub-questions** (essay-3 has Qs about individual diagram panels). Consider merging sub-questions.
4. **No user authentication** — state is per-browser, no sync across devices.

## Color scheme

Blue-based (`:root` in `index.css`):
- Primary: `#2563eb`, Deep: `#1e40af`, Soft: `#dbeafe`
- Accent: `#3b82f6`
- Correct/Wrong: green `#1f7a56` / red `#b65642`

## Deployment

- **GitHub Pages**: `.github/workflows/deploy.yml` auto-deploys on push to `main`
- **Netlify**: `netlify.toml` configured as fallback
- Build: `tsc -b && vite build` with `GITHUB_PAGES=true` env var for `/ZJU_Molecularbiology_tests/` base path

## Key architectural decisions

- **Type-first organization** (not chapter-first): 5 question types with nested subcategories
- **Self-judge for open-ended**: short-answer and essay never auto-grade
- **AI kept in pipeline**: distractor generation runs once via Python, frontend serves static JSON
- **Question type components isolated**: PracticePage is a thin dispatcher
- **Web Speech API for pronunciation**: browser-native, zero dependencies, used in flashcard review
