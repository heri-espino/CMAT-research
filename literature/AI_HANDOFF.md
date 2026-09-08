# AI handoff — literature

Read this file before literature searches, manuscript bibliography work, or adding new papers.

## Current architecture

The old migration-oriented `Bib/Bib2` organization has been replaced by a single canonical `library/`. Historical batch names remain only in Git history.

- `library/`: one physical copy of each article/version.
- `general/`: broad thematic navigation.
- `papers/paper1_ppa_persistence/`: editorial roles and missing literature for Paper 1.
- `papers/paper2_mu_performance/`: editorial roles and missing literature for Paper 2.

The current canonical library contains 50 Markdown article/version records and 49 PDFs. Docling assets are retained only for the original archived subset; the later expansion intentionally omitted its redundant PNG assets. `kahu_2018_student-engagement-educational-interface` currently has Markdown but no source PDF in the consolidated library.

## Paper 1

Question: whether formal academic-support use observed under the PPA1-linked first-year MU context persists into subsequent Calculus support use after that specific incentive is treated as no longer applying.

Target: *Studies in Higher Education*.

Literature balance: broad higher-education incentive/help-seeking/engagement framing first; mathematics support is the empirical setting rather than the entire theoretical contribution. Core anchors include Kahu, Fong, Karabenick, Agnew, Gneezy, Angrist, Pugatch, Paloyo and Blondeel. Hanushek & Woessmann (2008) is secondary institutional framing only.

Highest-priority missing comparator: Büchele & Schürmann (2024), *Studies in Higher Education*, DOI 10.1080/03075079.2023.2271029.

## Paper 2

Question: association between contemporaneous CMAT use and classroom-relative performance in first-attempt MU.

Target: TEAMAT first; IJMEST second.

Literature should be mathematics-support heavy. Current empirical interpretation to protect: the strongest separation is `0 visits` versus positive use; there is not robust evidence for a simple monotone 1→2→3→4+ dose-response. Core field anchors include Mullen, Lawson, Mac an Bhaird, Jacob, Berry, Matthews, Pell and Navarra-Madsen. Pugatch/Paloyo provide useful causal contrasts to the observational CMAT design.

Highest-priority missing items include Büchele & Schürmann (2024), Rickard & Mills (2018), and MacGillivray (2009 exact metadata/source).

## Retrieval policy

Do not rediscover a local paper on the web before checking the paper-specific index and `library/INDEX.md`. Read only relevant Markdown. Use the PDF when exact table/figure/numerical verification is necessary. Use the web for absent/current literature or metadata verification.

## Non-negotiable scientific language

CMAT visits are observational and student-selected. Do not infer causality, habits, intrinsic motivation, or psychological mechanisms from administrative visits. Use association/predictive association/pattern-consistent language.
