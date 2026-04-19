---
name: pdf
description: |
  Use when: "make pdf", "generate pdf", "convert to pdf", "pdf checklist", "regenerate pdf".
  Proactive: when a markdown deliverable is finalized and needs a human-facing PDF.
---

## Role
Document formatter. Convert markdown, text, or docx files into clean, paginated letter-size PDFs for human consumption.

## Prerequisites
- `pandoc` (brew install pandoc)
- `typst` (brew install typst)

Both are lightweight, no-sudo installs. The skill auto-checks and prompts if missing.

## Procedure

1. **Verify toolchain:**
   ```bash
   which pandoc && which typst
   ```
   If either is missing, run `brew install pandoc typst`.

2. **Identify the source file.** Accept `.md`, `.txt`, or `.docx`. If the user doesn't specify, check:
   - Current working directory for the most recently modified `.md`
   - `active/md/` for deliverables in the Truthly workspace

3. **Generate PDF with pandoc + typst engine:**
   ```bash
   pandoc "<input>" \
     -o "<output>.pdf" \
     --pdf-engine=typst \
     -V margin-top=0.75in \
     -V margin-bottom=0.75in \
     -V margin-left=0.85in \
     -V margin-right=0.85in \
     -V fontsize=10.5pt
   ```

4. **Verify output:**
   ```bash
   pdftotext "<output>.pdf" /tmp/_pdf_verify.txt
   wc -l /tmp/_pdf_verify.txt
   head -20 /tmp/_pdf_verify.txt
   tail -20 /tmp/_pdf_verify.txt
   ```
   Confirm: page count is reasonable, first and last sections are present, no truncation.

5. **Open for review:**
   ```bash
   open "<output>.pdf"
   ```

## Output Naming
- Same directory and base name as the input, with `.pdf` extension
- If input is `active/md/Foo.md`, output is `active/Foo.pdf` (PDFs go in `active/`, not `active/md/`)

## Customization Options
| Flag | Effect | Default |
|------|--------|---------|
| `--fontsize` | Body text size | 10.5pt |
| `--margin-*` | Page margins | 0.75in top/bottom, 0.85in left/right |
| `--toc` | Add table of contents | off |
| `--number-sections` | Number headings | off |

## Stop Conditions
- If source file doesn't exist, ask for the path.
- If `pdftotext` verification shows truncation or garbled text, report and retry.
- If pandoc/typst not installed and brew is unavailable, report BLOCKED.

## Why This Approach
Tried and discarded (March 2026):
- **weasyprint** — hangs in Claude Code sandbox (network/font resolution blocked)
- **Chrome headless** — hangs in sandbox (GPU process blocked)
- **Swift/WebKit createPDF** — renders but produces single tall page, text layer lost on pagination
- **textutil** — macOS native but doesn't support PDF output
- **pdflatex/xelatex/lualatex** — requires BasicTeX (needs sudo)

**pandoc + typst** works because: typst is a single Rust binary (no TeX distribution), produces proper multi-page PDFs with searchable text, respects pandoc's variable system for margins/fonts, and runs entirely offline with no sandbox issues.

## Chains
- Often follows a deliverable creation workflow (e.g., after editing a checklist or drafting an exhibit)
- Run `/verify` after if the PDF contains factual claims

## Adapted from
Custom skill. Not from gstack. Built March 26, 2026 after systematic trial of 6 PDF generation approaches in Claude Code's sandboxed environment.
