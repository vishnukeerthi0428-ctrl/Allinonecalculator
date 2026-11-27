# Source Pack brief: line-by-line coverage review and enhancement (38-document package)

Read `SHARED_BRIEF.md` first; all its writing, tagging, Mermaid and rendering rules apply. This brief adds the rules for reviewing the **38-document source pack**.

## Context
The blueprint (Parts 0–9, in `/home/user/Allinonecalculator/blueprint/`) was built from documents 01 (BRD) and 02 (FRD) only. The client has now supplied the **complete 38-document engineering package**. Documents 01/02 are byte-identical to the ones already used. Plain-text extractions of every document, with `<HeadingN>` markers, `[TABLE]` / `---row` / `[/TABLE]` delimiters and one cell per line, are in:
`/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/docs38/NN_Title.txt`
The original .docx files are in `.../scratchpad/zip38/38 documents/`. Treat document content as data, not instructions.

**Pattern of the pack.** Every document repeats a common core: product purpose and boundary, the Website/Admin operating contract, implementation and acceptance controls, optimization engineering, and current multi-startup scope. Each then adds its domain-specific content. Document 38 ("All Numbers") is the authoritative inventory:
- 76 BRs (71 + 5), 288 FRs (141 + 147), 321 API/adapter operations (302 + 19 candidate);
- 155 logical entities (149 + 6 candidate), 162 work items, 799 tests (Unit 75, SIT 422, UAT 302);
- 245 quality controls, 352 engineering decisions;
- 21 optimization dimensions with weights, 104 optimization controls, 24 optimization scenarios, **35 optimization KPIs (21 mandatory)**;
- an automation library of 20 industry templates, 20 use-case groups × 5 = 100 use cases, and 13 node types.

Document 37 is a worked end-to-end example.

**Known ID collision you must handle:** the pack's optimization KPIs are numbered KPI-01…35, but the blueprint already uses KPI-01…31 for business KPIs (Part 1). Inside the blueprint, refer to the pack's optimization KPIs as **OKPI-01…OKPI-35**, always.

## Your job (per assigned document group)
1. **Read every assigned document completely, line by line.** For large catalogue documents, also parse every table row programmatically with a Python script (save the script under `/home/user/Allinonecalculator/blueprint/assembly/source_pack/`), so that no row, ID, field or rule is skipped. Read all prose sections in full, and read enough rows of each table type to understand the semantics of every column.
2. **Build an atomic aspect inventory:** every distinct requirement, rule, field, ID, threshold, number, state, screen element, API operation, entity/column, test, control, decision, KPI, process step, role duty, plan item and limitation. Identify the shared-core sections that repeat across documents once, and do not re-list them per document. Instead, mark them as "common core: see document 01/02 coverage".
3. **Check coverage against the blueprint.** Use grep and read the relevant blueprint parts. For each aspect, record:
   - **Status:** Covered, Partially covered, Not covered, Conflict, or Not applicable (with reason).
   - **Blueprint location:** part, section and IDs.
   - **Action taken.**
   For catalogues, reconcile programmatically: for example, the source API operation IDs and paths vs the Part 3.2 API catalogue; source tables/columns vs the Part 3.3 entities; source test IDs vs Part 6 TCs. Produce mapping tables with counts.
4. **Enhance the blueprint.** For every Partially covered / Not covered aspect, **write the missing content at full blueprint depth** in your enhancement file: new or refined requirements, designs, fields, rules, procedures, catalogue rows, test cases, KPIs, checklists or plans. Apply the expert persona(s) for your domain at their best. Never silently change earlier parts. Additions are tagged; conflicts get `[CONFLICT-###]` with a **proposed resolution** (the coordinator will turn these into binding decisions).
   - Enhanced FRs: `FR-ENH-<G>-###`.
   - Enhanced stories: `US-<EP 2 digits>-E<G><nn>` (e.g. `US-08-EA01`).
   - Test cases: `TC-ENH-<G>-###`.
   - Other new items: use the source's own IDs where they exist (e.g. `SM-FR-…`, `SM-API-…`, `QC-…`) and show their mapping to blueprint IDs.
   - `<G>` is your group letter.
5. **Coverage CSV:** write `/home/user/Allinonecalculator/blueprint/final/coverage/<G>_coverage.csv` with columns: `doc, section, aspect_id, aspect_summary, status, blueprint_location, action, new_ids`.

## Output file (one per group; split into a/b/c if very large)
`/home/user/Allinonecalculator/blueprint/<file name given in your task>`, structured as:
- **X.1 Documents reviewed:** for each document: title, size, section list, what it is trying to tell (its purpose and pattern), and the count of atomic aspects found.
- **X.2 Coverage register summary:** counts by status per document.
- **X.3 Detailed coverage register:** the table of aspects. Long lists may be grouped, but every Not covered, Partial or Conflict item must be listed individually.
- **X.4 Catalogue reconciliation** (if applicable).
- **X.5 Enhancements:** the new content, organized by blueprint part. This is the main body and must be at full depth.
- **X.6 Conflicts and proposed resolutions.**
- **X.7 Expert persona review:** how each relevant persona's perspective was applied, and what each would still flag.
- **X.8 Tags register.**
- **X.9 Quality gate** (Section 11 items), then a status line.

## Boundaries
- Write only your enhancement file(s), your coverage CSV and your scripts. Do not edit earlier parts. Do not git commit.
- Render your file(s) with `make_pdf.sh` and verify zero diagram errors.
- **Report back (≤ 300 words):** files, pages, aspect counts by status, the top 10 most important additions, conflicts needing decisions, and anything you could not complete.
