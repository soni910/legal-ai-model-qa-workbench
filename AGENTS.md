# AGENTS.md

## Project
- **Project name:** Legal AI Model QA Workbench
- **Full title:** Legal AI Model QA Workbench: Contract Intelligence Dataset, Evaluation Harness, Error Taxonomy, and Annotation Guide.

## Purpose
This is a free portfolio project that simulates how a legal AI product specialist, contract-intelligence analyst, or model QA reviewer would test AI extraction of legal and business terms from contracts.

## Core Idea
Use synthetic contract excerpts, human-labeled gold-standard answers, simulated model outputs, error taxonomy, source-text checking, prompt-version tracking, and QA dashboards to demonstrate how legal/product/data-science teams can improve contract AI systems.

## Hard Constraints (Must Follow)
1. Use synthetic contract data only.
2. Do not use client data.
3. Do not provide legal advice.
4. Do not use paid APIs.
5. Do not use OpenAI API, Claude API, Gemini API, or external LLM APIs.
6. Do not use a database.
7. Do not add authentication.
8. Do not add secrets or API keys.
9. The app must be deployable on Streamlit Community Cloud.
10. Use Python, Streamlit, pandas, Altair, and pytest only.
11. Keep code simple and beginner-maintainable.

## App Pages
The Streamlit app should include and maintain these pages:
1. Project Overview
2. Dataset Browser
3. Gold Standard Labels
4. Prompt & Model Runs
5. Extraction Evaluation
6. Error Taxonomy
7. QA Dashboard
8. Improvement Recommendations
9. Annotation Guide

## Data Files (Required)
Do not remove or rename these expected files unless a change is explicitly planned and fully propagated:
- `contracts.csv`
- `excerpts.csv`
- `gold_labels.csv`
- `prompt_versions.csv`
- `model_runs.csv`
- `model_outputs.csv`
- `error_taxonomy.csv`
- `data_dictionary.csv`

## Evaluation Requirements
Evaluation logic should support:
- exact correctness
- partial correctness
- weighted scoring
- error type
- severity
- escalation_required
- source_match_status
- confidence calibration
- accuracy by field
- accuracy by contract type
- accuracy by prompt version
- high-confidence incorrect outputs
- model-instruction improvement recommendations

## Review Guidelines
1. Do not break CSV schemas.
2. Do not remove required columns.
3. Do not mix up `contract_id`, `excerpt_id`, `label_id`, `output_id`, and `run_id`.
4. Preserve synthetic-data disclaimers.
5. Preserve no-legal-advice disclaimers.
6. Keep dependencies minimal.
7. Do not add paid services.
8. Do not add external API calls.
9. Update tests when schemas change.
10. Do not overbuild.

## Definition of Done
A change is complete only when all are true:
- `python -m pytest` passes.
- `python scripts/predeploy_check.py` passes.
- `python -m compileall app.py pages utils scripts` passes.
- `python -m streamlit run app.py` launches.
- `README` explains the project to recruiters and legal AI product managers.
- All data is clearly marked synthetic.
- No proprietary vendor claims are made.
