# Agent Guidelines & Research Protocol

All AI coding assistants and autonomous agents operating within this repository MUST strictly abide by:
👉 [RESEARCH_RULES.md](file:///C:/Users/USER/RBL_ScamShield/RESEARCH_RULES.md)

### Key Directives for Agents:
1. **Never Hallucinate Citations or Metrics**: Always extract verified, exact numbers from papers. If information is absent, write `N/A`.
2. **Adhere to the Directory Structure**: Place data, scripts, results, figures, and manuscripts in their designated directories.
3. **No HARKing**: Keep research questions, baselines, and evaluation metrics locked prior to running test evaluations.
4. **Follow Git Conventions**: Format all commit messages using the required tags (`[SLR]`, `[GAP]`, `[DATA]`, `[MODEL]`, `[EXP]`, `[STAT]`, `[PAPER]`, `[DOC]`).
5. **Strict LLM Model Selection & Tier Constraints**:
   - **Gemini Models Floor:** NEVER call or configure any Google Gemini model lower than `gemini-3.5-flash` (strictly forbid `gemini-1.5-*`, `gemini-2.0-*`, `gemini-2.5-*`). Permitted Gemini models are: `gemini-3.5-flash-lite`, `gemini-3.5-flash`, `gemini-3.8-flash`, or higher.
   - **Claude Models Restriction:** Avoid calling Claude models unless explicitly required or when all primary and secondary maker-checker models in the standby chain fail.
   - **Primary & Benchmark Standard:** Standardize on `gpt-6.1-sol` (or equivalent tier models: `gpt-6-sol`, `gpt-5.6-sol`, `gemini-3.8-flash`) as the primary maker model across benchmark evaluations and forensic council specialists.
   - **Per-Sample Telemetry:** All batch runners and evaluation scripts MUST log the processing of each individual sample in real-time, detailing the sample ID, gold label, predicted label, latency, and exact count of API calls made.
6. **Standard Manuscript & Publication Format (JAIT Guidelines)**:
   - All manuscript drafts, section write-ups, and exports MUST strictly adhere to the **Journal of Advances in Information Technology** template (`docs/JAIT-template.doc`).
   - **Structure:** `I. INTRODUCTION`, `II. LITERATURE REVIEW`, `III. MATERIALS AND METHODS`, `IV. RESULT AND DISCUSSION`, `V. CONCLUSION`.
   - **Abstract Constraint:** Strictly between 150–250 words; self-contained with NO citations, NO hyperlinks, and NO undefined acronyms.
   - **Mandatory End-Matter:** Every submission must include `Conflict of Interest` ("The authors declare no conflict of interest."), `Author Contributions` (CRediT taxonomy), `Funding`, and `References` formatted as `Fig. 1.` / `TABLE I.`.


