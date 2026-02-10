
---

## `pyproject.toml`
**Propósito**: dependencias y metadata del proyecto

```toml
[project]
name = "etl_project"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
  "pandas",
  "psycopg2-binary",
  "python-dotenv",
  "pyyaml"
]
