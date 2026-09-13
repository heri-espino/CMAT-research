# Normalized controlled data (schema v2)

This directory is the relational representation intended for new CMAT analyses. It is additive: the flat pseudonymized files in `data/controlled/` remain unchanged so historical analyses can continue to use their original wide schemas.

Key design choices:

- `advisory_visits.timestamp` preserves the exact supplied date and clock time.
- Repeated career, subject and topic text is moved to dimensions and referenced through IDs.
- Student career is term- and source-specific rather than a permanent attribute of `students`, because program changes, multiple programs and administrative inconsistencies are possible.
- `careers.csv` links every current career to one of the five institutional schools.
- Advisory career labels are resolved against the current catalog conservatively; clear historical aliases are documented, while uncertain labels remain explicit rather than being silently forced to a current program.
- Academic `CLAVECARRERA` codes are linked to the current career catalog only when the code is itself current or when same-student/same-term diagnostic evidence is strong (top count >= 10 and top share >= 0.85). The evidence count and share remain in `career_codes.csv`.
- Conceptual subjects are separated from institutional course-code variants because multiple codes may share a name and four catalog codes have more than one historical name.
- `advisor_*` and academic `prof_*` remain separate namespaces until a verified professor-name-to-`CLAVEPROFESOR` crosswalk exists.
- `diagnostics.csv` recovers the legacy DMU diagnostic data with the same pseudonymized student IDs and no raw institutional IDs.

Generated tables:

```text
schools.csv
careers.csv
career_labels.csv
career_codes.csv
subjects.csv
course_variants.csv
subject_labels.csv
terms.csv
topics.csv
students.csv
instructors.csv
advisors.csv
student_careers.csv
course_attempts.csv
advisory_visits.csv
diagnostics.csv
NORMALIZATION_MANIFEST.json
SHA256SUMS.txt
```

All row-level files remain controlled pseudonymized research data. Normalization reduces redundancy but does not make the records anonymous.
