# SkyPoints Loyalty Program – Python ETL Pipeline

## 1. Project Overview

This project implements a Python-based ETL pipeline for the SkyPoints airline loyalty program technical assessment.

The source system provides two daily feeds:
- A pipe-delimited member profile file.
- A semi-structured JSON redemption feed.

The pipeline discovers and reads both feeds, validates records, transforms accepted data, routes members by country, processes redemption transactions, and joins redemption records with member profiles.

**Scope:** This README documents the Python batch implementation. Snowflake utilities or a separately tested Snowflake pipeline are not invoked by `python -m src.pipeline.main`.

## 2. Workflow

```text
Member Profile File                 Redemption JSON
        |                                  |
        v                                  v
  File Discovery                     File Discovery
        |                                  |
        v                                  v
  Read / Standardize                 Read / Parse JSON
        |                                  |
        v                                  v
  Profile Validation                 Redemption Validation
     /       \                             |
 Accepted  Rejected                        v
    |         |                      Transform Dates
    v         v                            |
Transform   Rejected                       v
Dates       CSV                      Accepted Transactions
    |                                      |
    v                                      |
Calculate AGE                              |
Calculate STALE_MEMBER                     |
    |                                      |
    v                                      |
Country Routing                            |
    |                                      |
    v                                      v
Country CSV Files                    Join by MEMBER_ID
                                           |
                                           v
                                    Joined Output CSV
```

## 3. Main Features

### Member profiles
- Discovers profile files and reads header (`H`) and detail (`D`) records.
- Standardizes column names.
- Validates mandatory fields, duplicate member IDs, field lengths, and date values.
- Separates accepted and rejected records.
- Transforms date fields.
- Calculates `AGE` from `DOB`.
- Calculates `STALE_MEMBER` from `LAST_FLIGHT_DATE`.
- Splits accepted members by `COUNTRY`.

### Redemption transactions
- Discovers and parses JSON redemption files.
- Supports a single JSON object or a list of objects.
- Validates required fields, duplicate transaction IDs, dates, and non-negative miles.
- Transforms feed and transaction dates.
- Produces accepted and rejected redemption outputs.

### Member-redemption join
- Joins accepted redemption transactions to accepted member profiles using `MEMBER_ID`.
- Uses a left merge with merge indicators to identify matched and unmatched transactions.

## 4. Business Rules and Derived Fields

| Field | Rule |
|---|---|
| `AGE` | Calculated from `DOB` using the current date and accounting for whether the birthday has occurred this year. |
| `STALE_MEMBER` | `Y` when days since `LAST_FLIGHT_DATE` is greater than 90; otherwise `N`. |
| Missing `DOB` | Age is null. |
| Missing `LAST_FLIGHT_DATE` | Stale-member flag is null. |
| Country routing | Accepted member records are split using `COUNTRY`. |

The current date transformation supports `YYYYMMDD` for enrollment and last-flight dates. DOB parsing supports `DDMMYYYY` and `YYYYMMDD`, as defined in the transformation module.

**Join-key assumption:** Redemption records contain `member_id`, so the join uses `MEMBER_ID`. This assumes member IDs are globally unique. If IDs can repeat across countries, the source must provide another disambiguating key.

**Latest-record assumption:** The implementation includes latest-record handling logic and tests. The supplied source format does not contain a source update timestamp or sequence. Ingestion order cannot guarantee the true latest source update if files arrive out of order.

## 5. Technology Stack

- Python
- Pandas
- Pytest
- Python standard library (JSON, dates, file and path handling)
- Dependencies listed in `requirements.txt`

## 6. Project Structure

```text
data_engineering_assessment/
├── config/                 # Configuration, if used
├── data/
│   └── processed/
│       ├── members/        # Country-specific member CSV files
│       ├── rejected/       # Rejected member records
│       ├── redemptions/    # Accepted and rejected redemption data
│       └── joined/         # Joined redemption/member output
├── docs/                   # Documentation
├── logs/                   # Logs, if configured
├── sql/                    # SQL artifacts, if retained
├── src/
│   ├── database/           # Separate database connection/load utilities
│   ├── ingestion/          # File discovery and source readers
│   ├── pipeline/           # Main pipeline and output writers
│   ├── standardization/    # Column standardization
│   ├── transformation/     # Date, derived-column, country and join logic
│   └── validation/         # Profile, redemption and data-quality checks
├── tests/                  # Automated tests
├── requirements.txt
└── README.md
```

## 7. Setup

Prerequisites: Python installed. The commands below use Windows PowerShell.

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 8. Input Files

Place source files in the input location configured by `src/ingestion/file_discovery.py`. Confirm supported extensions and directory settings in that module before execution.

Example profile records:

```text
|H|Member_Name|Member_Id|Enrollment_Date|Last_Flight_Date|Tier_Code|Agent_Name|State|Country|DOB|Is_Active
|D|Elena|223457|20101012|20121013|GLD|Sam|CA|USA|03051985|A
```

Example redemption JSON:

```json
{
  "member_id": "223457",
  "feed_date": "20240115",
  "redemptions": [
    {
      "txn_id": "RX10091",
      "txn_date": "20240110",
      "partner": "AeroLink",
      "miles_redeemed": 12000,
      "status": "COMPLETED"
    }
  ]
}
```

## 9. Run the Pipeline

From the project root with the virtual environment activated:

```powershell
python -m src.pipeline.main
```

The pipeline prints file counts, accepted and rejected record counts, country-wise member counts, and redemption join results.

## 10. Output Files

The pipeline writes CSV outputs under `data/processed/`:

```text
data/processed/
├── members/
│   ├── usa_members.csv
│   ├── ind_members.csv
│   ├── phil_members.csv
│   ├── can_members.csv
│   └── au_members.csv
├── rejected/
│   └── rejected_members.csv
├── redemptions/
│   ├── accepted_redemptions.csv
│   └── rejected_redemptions.csv
└── joined/
    └── redemption_member_details.csv
```

The actual country files depend on the country routing configuration and input data.

## 11. Run Tests

```powershell
python -m pytest -v
```

At the time of preparation, the observed test run reported **26 passed, 0 failed**. Tests cover file discovery and parsing, standardization, validation, date transformations, derived fields, country routing, latest-record handling, redemption parsing, and redemption/member joining.

Re-run the tests after changes; this result records the observed run and is not a guarantee for future changes.

## 12. Validation and Rejection Handling

The pipeline separates invalid records from accepted records. Implemented validation includes mandatory values, duplicate identifiers, field-length constraints, date validity, non-negative redemption miles, and other checks in the validation modules. Rejected records are written to dedicated CSV outputs for review.

## 13. Scalability Considerations

The current implementation is a local Python/Pandas batch pipeline demonstrated with sample data. It has **not** been benchmarked or demonstrated processing billions of records.

Potential production-scale improvements include:
- Processing files in chunks or manageable batches.
- Avoiding loading all records into memory and repeated full-data concatenations.
- Using distributed processing, such as Spark, when a single-machine Pandas workload is insufficient.
- Writing partitioned columnar outputs such as Parquet where appropriate.
- Adding idempotent ingestion, durable checkpoints, retries, monitoring, and operational alerting.
- Using a source-provided update timestamp or sequence to resolve out-of-order updates correctly.
- Defining retention, recovery, and data-quality reporting policies.

These are proposed improvements, not capabilities claimed by the current sample-data implementation.

## 14. Assumptions and Limitations

- The join uses `MEMBER_ID` and assumes it is globally unique.
- The source feed does not provide a reliable source-update timestamp or sequence for out-of-order latest-record resolution.
- DOB parsing supports the formats configured in the date transformation module.
- Missing DOB and last-flight dates result in null derived values, as described above.
- The current implementation is a local batch solution, not a distributed billion-record deployment.
- Database utilities in `src/database/` are separate from the Python batch command documented here.

## 15. Assessment Deliverables Mapping

| Assessment deliverable | Python implementation |
|---|---|
| Raw, staging and country-target table DDL | Not included in this Python-only execution scope. |
| Age and stale-member derived fields | Implemented in Python transformations. |
| Country segregation and latest-record handling | Implemented in Python processing/routing logic and covered by tests. |
| JSON transaction processing and member join | Implemented in Python redemption processing and join logic. |
| Data validation | Implemented in Python validation modules and covered by tests. |
| Live demonstration | Run the pipeline and test suite using the commands above. |

If the reviewer expects the table-DDL deliverable in the submitted repository, include the relevant SQL DDL as a separate artifact or clarify that this submission is limited to the Python approach. This README does not claim that Python code substitutes for database DDL.

## 16. Suggested Demonstration

1. Show the source profile and redemption files.
2. Explain the ingestion, validation, and transformation modules.
3. Run `python -m src.pipeline.main`.
4. Explain accepted and rejected record counts.
5. Inspect country-specific member CSV files.
6. Inspect accepted and rejected redemption CSV files.
7. Inspect the joined output and explain the `MEMBER_ID` join.
8. Run `python -m pytest -v`.
9. Discuss assumptions and production-scale improvements.
