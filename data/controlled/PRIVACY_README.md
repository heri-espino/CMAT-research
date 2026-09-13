# Privacy / pseudonymization

This research release preserves the substantive advisory variables required for analysis: exact timestamp, carrera, semestre, profesor, materia, tema, and periodo.

Original student identifiers are replaced by deterministic `stu_*` HMAC-SHA256 pseudonyms that are identical across Materias and Asesorias. Academic `CLAVEPROFESOR` values are replaced by deterministic `prof_*` pseudonyms.

The advisory `profesor` field contains professor names, whereas the supplied Materias file contains only numeric `CLAVEPROFESOR`; because no verified name-to-ID crosswalk is present, advisory professor names are currently represented by deterministic `advisor_*` pseudonyms. They must not be interpreted as linked to `prof_*` identifiers until a verified crosswalk is supplied.

No substantive advisory fields are removed, and the exact supplied timestamp is retained.

This is pseudonymization, not anonymization. The combination of timestamp, career, semester, course, topic, grade, and longitudinal patterns can remain identifying. These files are controlled research data and may be stored in this repository only while it remains private with access limited to authorized collaborators. The HMAC key is not included and must remain outside Git.
