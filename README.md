# enrich-o11y-metrics

A utility to enrich Splunk Observability Cloud metrics by adding **custom properties and tags** to host metrics after ingestion.

This enables improved filtering, grouping, metadata standardisation, and contextual analysis of infrastructure metrics in Splunk Observability Cloud.

---

## Overview

`update_dimensions` reads a `hosts.csv` file containing host metadata and updates the corresponding `host.name` dimension in Splunk Observability Cloud.

The script supports:

- **Custom Properties** — key/value metadata such as Environment, Business Owner, Compliance Zone, Location, etc.
- **Tags** — multi-value labels associated with a host.

---

## Prerequisites

Before running the script, update the following configuration values in the script:

```python
API_TOKEN = "YOUR_USER_API_TOKEN"

API_BASE = "https://api.<REALM>.signalfx.com/v2/dimension/host.name/"
```

### Parameters

| Parameter | Description |
|------------|-------------|
| `API_TOKEN` | Splunk Observability Cloud User API Token |
| `REALM` | Splunk Observability Cloud realm (e.g. `us1`, `eu0`, `au0`) |

Example:

```python
API_TOKEN = "abc123xyz"

API_BASE = "https://api.au0.signalfx.com/v2/dimension/host.name/"
```

---

## Input File

The script expects a file named `hosts.csv` located in the **same directory** from which the script is executed.

### Example CSV Format

```csv
host,Env,Business Owner,Compliance Zone,Location,tags
APP-01,Dev,IT,Non Regulated,USA,TAG1
APP-02,Prod,Finance,Regulated,Australia,TAG1|TAG2|TAG3
```

---

## CSV Schema

### Fixed Columns

The following columns have predefined behaviour:

| Column | Description |
|---------|-------------|
| `host` | Required. Host name used to identify the target `host.name` dimension in Splunk Observability Cloud |
| `tags` | '|' separated list of tags |

Example:

```csv
APP-02,...,TAG1|TAG2|TAG3
```

---

### Dynamic Columns

All columns other than `host` and `tags` are treated as **custom properties**.

The column name becomes the property key and the cell value becomes the property value.

Example:

| Column | Value |
|---------|-------|
| Env | Dev |
| Business Owner | IT |
| Compliance Zone | Non Regulated |
| Location | USA |

These are automatically mapped into Splunk Observability Cloud custom properties.

---

## Rules

- Each row represents **one host**
- Values are **comma separated**
- All columns except `tags` accept **a single value**
- `tags` supports **multiple values separated by `|`**
- Additional metadata columns can be added without modifying the script between host and tags columns

---

## Example Mapping

Input CSV:

```csv
host,Env,Location,tags
APP-01,Dev,USA,TAG1|TAG2
```

---

## Running the Script

Place `hosts.csv` in the same directory and execute:

```bash
python update_dimensions.py
```

---

## Use Cases

- Add operational metadata to hosts after metric ingestion
- Standardise environment and ownership information
- Enable richer filtering and grouping in dashboards and detectors
- Bulk update tags and custom properties using CSV input
