# enrich-o11y-metrics

A utility to enrich Splunk Observability Cloud metrics by adding **custom properties and tags** to host-based metrics after ingestion.

This helps improve filtering, grouping, and contextual analysis of infrastructure metrics in Splunk Observability Cloud.

---

## Overview

`enrich-o11y-metrics` reads a CSV file containing host name and metadata (that needs to be added) and updates corresponding metric dimensions in Splunk Observability Cloud by attaching:

- Custom properties (e.g., environment, owner, compliance zone)
- Tags (multi-valued labels)

---

## Input File

The tool expects a `hosts.csv` file in the same directory from where the script is executed.

### Example Format

```csv
host,Env,Business Owner,Compliance Zone,Location,tags
APP-01,Dev,IT,Non Regulated,USA,TAG1
APP-02,Dev,IT,Non Regulated,USA,TAG1|TAG2|TAG3


