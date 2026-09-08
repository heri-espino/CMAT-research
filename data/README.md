# Data policy

Raw administrative data are intentionally **not stored in GitHub**.

The analysis expects controlled local inputs such as:

- official academic records with course attempts/final grades;
- CMAT visit records linked internally through institutional student ID;
- future approved pre-treatment measures such as mathematics-admission/diagnostic scores;
- future survey responses about reasons for CMAT use, if collected and approved.

These files may contain direct or indirect identifiers and must remain in the institutionally controlled environment.

## What may be committed

- schemas/dictionaries with no identifying values;
- synthetic examples;
- source-file SHA-256 hashes for provenance;
- privacy-reviewed aggregated statistics;
- code that reads local data through configurable paths.

## What must not be committed

- student IDs;
- names/emails;
- row-level academic histories;
- raw CMAT Forms exports;
- identifiable free text;
- HMAC keys or salts;
- access credentials;
- privately licensed source files unless explicitly approved.

A SHA-256 checksum proves integrity/version identity only. It does not anonymise a dataset.
