# Data Origins

Raw data lives in `data/raw/`. These files are **not versioned** — they are
downloaded from WHO and kept locally for reproducibility.

## Sources

| Dataset | Source | License |
|---------|--------|---------|
| ICD-10 2019 (ClaML) | WHO ICD-10 Download Page | CC BY-ND 3.0 IGO |
| ICD-11 MMS SimpleTabulation | WHO ICD-11 Download Area | CC BY-ND 3.0 IGO |
| ICD-10 to ICD-11 Mapping | WHO ICD-11 Mapping Tables | CC BY-ND 3.0 IGO |

### Download URLs

- **ICD-10**: <https://icdcdn.who.int/icd10/claml/icd102019en.xml.zip>
- **ICD-11**: <https://icdcdn.who.int/static/releasefiles/2024-01/SimpleTabulation-ICD-11-MMS-en.zip>
- **Mapping**: <https://icdcdn.who.int/static/releasefiles/2024-01/mapping.zip>

## SHA-256 Hashes

```
344c571aa9aed3b9ad1c80261b7828c45cfb5fc0b1a5da64aecef354dff5b3d9  icd102019en.xml.zip
b92212138c67738aa4770f5fae5bbdf43ebb98632086df3fd47b5bed954d9216  SimpleTabulation-ICD-11-MMS-en.zip
ef1370361a3fe5e414e6f1c75b84a8aa04f4d937744c429ce51e9728a81445e2  mapping.zip
```

## Directory Structure

```text
data/raw/
├── icd10/
│   ├── icd102019en.xml.zip          # Original ZIP
│   └── icd102019en.xml              # Extracted ClaML XML
├── icd11/
│   ├── SimpleTabulation-ICD-11-MMS-en.zip   # Original ZIP
│   ├── SimpleTabulation-ICD-11-MMS-en.txt   # Tabular text
│   ├── SimpleTabulation-ICD-11-MMS-en.xlsx  # Tabular Excel
│   └── readme.txt                             # WHO readme
└── mapping/
    ├── mapping.zip                              # Original ZIP
    ├── 10To11MapToMultipleCategories.txt/.xlsx  # ICD-10 → ICD-11 (one-to-many)
    ├── 10To11MapToOneCategory.txt/.xlsx         # ICD-10 → ICD-11 (one-to-one)
    ├── 11To10MapToOneCategory.txt/.xlsx         # ICD-11 → ICD-10 (one-to-one)
    ├── foundation_10To11MapToOneCategory.txt/.xlsx  # Foundation mapping (10→11)
    └── foundation_11To10MapToOneCategory.txt/.xlsx  # Foundation mapping (11→10)
```

## Notes

- `mapping/` is **ground truth only** — used for validation, not direct computation.
- All data is in English.
- ICD-10 uses ClaML XML format (ClaML = Classification Markup Language).
- ICD-11 SimpleTabulation provides a flattened tabular view of the MMS linearization.
