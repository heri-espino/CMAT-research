# Local raw data

This directory is the canonical local location for controlled CMAT administrative inputs. The directory exists in Git only through this README; all actual raw files are ignored and must remain on the authorized local/institutional environment.

Place the source workbooks here after cloning:

```text
data/raw/
├── Materias estudiantes-profesores 2019-2025 P y O.xlsx
├── Asesorias2024.xlsx
└── pre_treatment_covariates.xlsx   # optional, only when approved/available
```

The shared configuration also accepts the shorter local aliases `Materias.xlsx` and `Asesorias.xlsx`, but the filenames above are the canonical names used by the current CMAT source files.

Paper and shared-study runners that use `cmat_analysis.config.study_config.get_study_config()` will discover these files automatically, so normal local runs do not need `--materias` or `--asesorias` when the canonical files are present here. Explicit CLI paths still override the defaults.

For temporary backward compatibility, the configuration can still find the same raw filenames directly under `data/`, as well as privacy-reviewed anonymized CSV inputs when those are the only available inputs. New local setups should use `data/raw/`.

Do not commit student IDs, names, emails, row-level academic records, raw Google Forms/CMAT exports, identifiable free text, keys, salts, or credentials. See `../README.md` for the repository data policy.
