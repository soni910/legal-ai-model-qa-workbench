# Annotation & Escalation Guide

**Project:** Legal AI Model QA Workbench  
**Dataset context:** Synthetic contract excerpts only  
**Audience:** Legal AI product specialists, QA reviewers, annotation leads, hiring managers

---

## 1) Purpose
This guide defines a practical, repeatable annotation and escalation workflow for evaluating contract-intelligence extraction outputs.

It is designed to help teams:
- score extraction quality consistently
- separate model errors from annotation ambiguity
- identify high-risk failure patterns early
- communicate clearly across legal, product, and data-science stakeholders

---

## 2) Scope
This guide applies to:
- synthetic contract excerpts in this repository
- gold-label creation and review
- model-output evaluation against gold labels
- escalation decisions for ambiguous or high-risk outputs

This guide does **not** provide legal advice and does not apply to client/proprietary data.

---

## 3) Field Definitions
Use these field classes consistently during annotation and review:

- **governing_law**: jurisdiction governing contract interpretation
- **contract_term**: duration/start-end structure of the agreement
- **renewal_type / auto_renewal**: renewal mechanics and timing
- **termination_for_convenience / termination_for_cause**: termination rights and triggers
- **notice_period**: formal notice timing requirements
- **limitation_of_liability / liability_cap_amount / exclusions_from_liability_cap**: cap amount and carve-outs
- **indemnity**: indemnity obligations and party assignment
- **data_security_obligation**: security commitments and controls
- **confidentiality_survival_period**: post-termination confidentiality duration
- **assignment_change_of_control**: assignment permissions/restrictions
- **audit_rights**: audit entitlement and conditions
- **payment_terms / late_payment_interest**: payment cycle and late-fee mechanics
- **most_favoured_customer**: parity pricing obligations
- **non_solicit**: workforce solicitation restrictions
- **subcontracting_rights**: use of subcontractors and accountability

---

## 4) What Counts as a Positive Match
A positive match requires:
1. **Correct value extraction** for the target field.
2. **Correct scope** (right party, clause scope, and qualifier context).
3. **Source support** in the cited excerpt text.
4. **No critical omissions** of carve-outs that change interpretation.

Operationally:
- **correct** = fully aligned value + scope + support
- **mostly_correct** = minor non-material wording differences
- **partial** = captures some but not all critical parts

---

## 5) What Does *Not* Count as a Positive Match
Do not mark positive when any of the following occurs:
- wrong party attributed obligation
- wrong time period or amount
- answer contradicts explicit clause language
- missing key exception/carve-out
- source text does not support answer
- definitive answer given to materially ambiguous language without escalation

---

## 6) Source-Text Requirements
Every assessed extraction should include a source check:
- **supported**: citation directly supports extracted value
- **partially_supported**: citation supports part of answer only
- **unsupported**: citation does not support the answer

Reviewer standard:
- prefer short, direct textual evidence
- reject broad citations that do not anchor the exact value
- flag cross-reference dependency when excerpt alone is insufficient

---

## 7) Confidence Scoring Guidance
Confidence should reflect expected correctness, not answer fluency.

Recommended interpretation:
- **low (0.00–0.39)**: weak evidence or uncertain parse
- **medium (0.40–0.69)**: partially reliable extraction
- **high (0.70–1.00)**: strong evidence and low uncertainty

Critical QA rule:
- high-confidence + incorrect output is a **priority risk** and should be highlighted.

---

## 8) Error Taxonomy
Use these categories consistently:
- False positive
- False negative
- Scope error
- Party error
- Time-period error
- Monetary error
- Exception error
- Cross-reference error
- Source support error
- Ambiguity escalation

When multiple errors are possible, choose the **primary driver** of wrong outcome.

---

## 9) Severity Rules
Severity is impact-oriented:
- **low**: minor wording mismatch, low decision impact
- **medium**: materially incomplete output, moderate risk
- **high**: likely to mislead legal/commercial decision-making

Default high-severity triggers:
- liability cap/exclusion errors
- monetary extraction errors
- party-attribution reversals
- escalation failures on legal ambiguity

---

## 10) Escalation Rules
Set `escalation_required = true` when:
- clause ambiguity changes legal/commercial interpretation
- output conflicts with monetary or liability-critical terms
- exceptions materially alter baseline rule
- evidence is incomplete due to unresolved cross-reference context

Escalation destination should be role-specific:
- legal SME for interpretation-sensitive ambiguity
- product owner for UX/flow risks
- data science for repeat model-failure signatures

---

## 11) Product Ambiguity vs Model Ambiguity vs Legal Ambiguity
- **Product ambiguity**: unclear rubric/UI behavior (review process issue)
- **Model ambiguity**: extraction uncertainty from model behavior (prediction issue)
- **Legal ambiguity**: clause language itself supports multiple interpretations (substantive issue)

Reviewer action:
- classify ambiguity source first, then decide whether to escalate.

---

## 12) Quality-Control Checklist
Before finalizing a review batch, confirm:
- [ ] IDs align (`contract_id`, `excerpt_id`, `label_id`, `run_id`, `output_id`)
- [ ] field_name matches rubric definition
- [ ] match_status aligns with evidence
- [ ] score aligns with match_status rubric
- [ ] source support status is justified
- [ ] error_type and severity are coherent
- [ ] escalation flag is applied where needed
- [ ] notes are concise and decision-useful

---

## 13) Borderline Examples
**Example A: Partial with acceptable core value**  
- Clause includes main value + exception. Model extracts main value only.  
- Outcome: `partial`, `Exception error`, likely `medium` or `high` based on impact.

**Example B: Wording mismatch but same legal effect**  
- Model says “net 30 days,” clause says “due within 30 days.”  
- Outcome: `mostly_correct` if source support is direct.

**Example C: Ambiguous clause answered definitively**  
- Clause uses conditional language with unresolved reference.  
- Model gives definitive output at high confidence.  
- Outcome: `incorrect` or `ambiguous`, `Ambiguity escalation`, likely `high` severity.

---

## 14) Suggested Model-Instruction Improvements
When recurring errors are detected, prioritize instruction updates that:
- force extraction of exceptions alongside base rule
- require explicit party-role tagging
- require answer + supporting snippet pairs
- enforce ambiguity-aware behavior (`escalation_required=true` when uncertainty indicators exist)
- add field-specific extraction hints for historically weak fields

---

## 15) Reviewer Sign-Off Checklist
For employer-facing rigor, reviewers should sign off only when:
- [ ] scoring is consistent across sampled records
- [ ] high-confidence incorrect outputs are explicitly reviewed
- [ ] high-severity items are triaged with ownership
- [ ] escalation-required records are routed appropriately
- [ ] recommendation output is actionable for product + DS + legal collaboration
- [ ] synthetic-data and no-legal-advice constraints remain preserved

---

### Portfolio Positioning Note
This guide is intentionally practical and cross-functional so employers can evaluate:
- annotation discipline
- QA risk judgment
- communication clarity
- ability to convert model errors into product and instruction improvements
