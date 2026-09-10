# cmat_analysis API review backlog

This file records non-blocking semantic/API questions that were intentionally left unchanged during the 0.2.0 architecture and documentation refactor. They require explicit repo-admin and scientific review before any deprecation, rename, consolidation, or behavioral change.

## 1. Overlapping clustered omnibus APIs

The pairs `clustered_visit_group_omnibus` / `clustered_omnibus_visit_group_test` and `clustered_career_omnibus` / `clustered_omnibus_career_test` appear semantically close. Do not deprecate or merge them based only on naming similarity. Review their estimands, implementation differences, return contracts, current consumers, and historical outputs before deciding whether both remain public.

## 2. Historical imputation API versus current outcome construction

`preprocessing.get_salones_with_imputations` remains public because it supports a historical/report-compatible procedure, while `measures.add_primary_outcomes` represents current primary outcome construction. Their coexistence is documented but deserves a later API review. Do not silently substitute one for the other or reinterpret historical outputs.

## 3. Revalidation classification is probabilistic/administrative inference

`ppa.classify_revalidation_records` infers likely administrative/revalidation categories from available records; the source extract does not contain an observed revalidation flag. Preserve `likely_*` terminology and do not present these categories as directly observed truth unless new authoritative data become available.

## 4. Temporal peaks are not exam dates

Temporal peak and periodicity diagnostics cannot identify examination dates or causal responses to assessments without an official exam calendar. Keep interpretations limited to temporal patterns compatible with academic rhythms.

## 5. `SEMESTER_LAG` naming

`SEMESTER_LAG` remains a historical alias of `ACADEMIC_TERM_LAG`, although the period index can include Primavera, Verano, and Otoño. Renaming or deprecating the alias would be an API change and should be handled separately with consumer search, migration notes, and compatibility policy.

## Review rule

These items are not defects to fix opportunistically. Any change must be separated from unrelated refactors, preserve or explicitly migrate historical consumers, add targeted tests, update `PUBLIC_API.md`/Sphinx when public API changes, and record scientific implications when relevant.
