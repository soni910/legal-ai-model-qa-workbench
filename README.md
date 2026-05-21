# Legal AI Model QA Workbench

**Full title:** Legal AI Model QA Workbench: Contract Intelligence Dataset, Evaluation Harness, Error Taxonomy, and Annotation Guide.

## What this is
This is an employer-facing **simulated contract-intelligence QA workbench**.

It demonstrates how legal AI product, QA, and contract-intelligence teams can evaluate contract term extraction quality using:
- synthetic contract excerpts
- gold-standard labels
- model run comparisons
- error taxonomy and severity tracking
- escalation workflows across legal, product, and data science

## What this project is **not**
- Not legal advice
- Not a production legal AI system
- Not trained on customer/proprietary contracts
- Not integrated with external paid APIs or external LLM APIs

## Skills Demonstrated
- contract analysis
- legal AI model evaluation
- annotation guide drafting
- error taxonomy design
- product/legal/data-science communication
- QA dashboard design
- synthetic dataset design
- model-instruction improvement

## How an employer should review this
1. Start with **Project Overview**.
2. Review **Synthetic Dataset** in Dataset Browser.
3. Review **Gold Standard Labels**.
4. Review **Extraction Evaluation**.
5. Review **QA Dashboard**.
6. Review **Annotation Guide**.


## QA methodology
Use these fields together as a decisioning framework:

- **match_status**: qualitative correctness class (`correct`, `mostly_correct`, `partial`, `incorrect`, `not_present`, `ambiguous`, `not_assessable`).
- **score**: quantitative severity of correctness for aggregate tracking (e.g., 1.0 correct, 0.75 mostly_correct, 0.5 partial, 0.25 minimally_correct, 0.0 incorrect).
- **severity**: business/legal risk level of the error (`low`, `medium`, `high`) used for triage priority.
- **escalation_required**: explicit routing flag for cross-functional follow-up (legal SME, product, or data science).

Recommended decision flow:
1. Validate extraction correctness with **match_status** and **score**.
2. Prioritize remediation using **severity** (high first).
3. Route ambiguous/high-risk rows when **escalation_required=true**.
4. Use recurring patterns to drive prompt changes, annotation-guide updates, and product guardrails.

## Why this is credible
- Traceability from source text → gold label → model output → score.
- Explicit error taxonomy and severity/escalation fields.
- Dedicated review workflow for high-confidence incorrect outputs.
- Practical annotation and escalation guide for cross-functional teams.

## Current maturity (honest scope)
This is a portfolio MVP focused on QA workflow design. It intentionally does **not** include:
- production authentication
- database infrastructure
- live LLM integrations
- legal document ingestion pipelines

## Important constraints
- Synthetic contract data only
- No proprietary Workday, Evisort, customer, or confidential data
- No legal advice
- No paid APIs
- No external LLM API calls

## Local run
```bash
pip install -r requirements.txt
python -m streamlit run app.py
```
