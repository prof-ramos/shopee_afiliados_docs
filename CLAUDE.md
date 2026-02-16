# CLAUDE.md

## Project Overview

**shopee_afiliados_docs** is an unofficial Python client library for the Shopee Affiliate API (Brazil). It provides a GraphQL-based client with SHA256 authentication, retry logic with exponential backoff, pagination support, and sub-ID tracking for affiliate links.

- **Language:** Python (>=3.10)
- **Package manager:** [uv](https://github.com/astral-sh/uv) (preferred over pip)
- **License:** MIT
- **Version:** 0.1.0 (Beta) / internal package version 1.0.0

## Repository Structure

```
src/shopee_affiliate/          # Main Python package
  __init__.py                  # Package exports, version
  client.py                   # Public API client (ShopeeAffiliateClient)
  transport.py                # HTTP layer with retry/backoff
  auth.py                     # SHA256 signature generation
  queries.py                  # GraphQL query builders
  validators.py               # Input validation (sub-IDs)
  graphql/                    # GraphQL template files (.graphql)
tests/
  unit/                       # Unit tests (no external deps)
  python/                     # Integration tests (require API credentials)
examples/python/              # Usage examples
docs/                         # Extensive documentation (Portuguese)
scripts/                      # Utility and automation scripts
benchmarks/                   # Performance benchmarks
.github/
  workflows/ci.yml            # CI pipeline (lint, test, security, build)
  workflows/release.yml       # Release automation
  dependabot.yml              # Dependency update config
```

## Development Setup

### Prerequisites

- Python 3.10+ (tested against 3.10, 3.11, 3.12, 3.13)
- uv package manager

### Installation

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
uv pip install -r requirements-dev.txt
```

### Environment Variables

Copy `.env.example` to `.env` and fill in credentials:
```
SHOPEE_APP_ID=your_app_id
SHOPEE_APP_SECRET=your_app_secret
```

**Never commit `.env` files.** They are in `.gitignore`.

## Common Commands

### Running Tests

```bash
# All tests
pytest tests/ -v --tb=short

# Unit tests only (no API credentials needed)
pytest tests/ -v --tb=short -m "not integration"

# Integration tests only (requires .env credentials)
pytest tests/ -v --tb=short -m integration

# Specific test file
pytest tests/unit/test_auth.py -v
```

### Linting and Formatting

```bash
# Check lint
ruff check src/ tests/

# Check formatting
ruff format --check src/ tests/

# Auto-fix lint issues
ruff check --fix src/ tests/

# Auto-format
ruff format src/ tests/
```

### Type Checking

```bash
mypy src/ --ignore-missing-imports
```

### Security Scanning

```bash
bandit -r src/
safety check
```

### Building

```bash
python -m build
twine check dist/*
```

## Architecture

The codebase follows a layered architecture:

1. **Client Layer** (`client.py`) - Public API with typed methods for each endpoint
2. **Transport Layer** (`transport.py`) - HTTP communication, retry logic with exponential backoff, respects `Retry-After` headers
3. **Auth Layer** (`auth.py`) - SHA256 HMAC signature generation using canonical JSON
4. **Query Layer** (`queries.py`) - GraphQL query template rendering using `re.sub()` for performance
5. **Validation Layer** (`validators.py`) - Input validation (sub-ID format, count limits)

### API Endpoints

The client supports 5 GraphQL endpoints:
- `shopeeOfferV2` - Shopee platform offers
- `shopOfferV2` - Shop-level offers
- `productOfferV2` - Product-level offers
- `conversionReport` - Conversion/commission reports (paginated via scrollId)
- `generateShortLink` - Affiliate short link generation (mutation)

### Base URL

```
https://open-api.affiliate.shopee.com.br/graphql
```

## Code Conventions

### Style

- **PEP 8** compliant, enforced by ruff
- 4 spaces for indentation
- `snake_case` for functions/variables, `PascalCase` for classes
- Type hints on all public functions (`from __future__ import annotations`)
- Docstrings on public classes and methods
- Double quotes for strings

### Return Types

All API methods return raw `dict` (JSON) rather than DTOs - this is an intentional design decision for flexibility.

### Error Handling

- Transport retries on HTTP 429, 500, 502, 503, 504
- Maximum 4 retry attempts with configurable backoff
- Sub-ID validation: alphanumeric only, max 5 items (prevents API error 11001)

### Performance

- GraphQL template rendering uses `re.sub()` instead of `.replace()` (8.46x faster)
- Pagination uses iterator patterns (`iter_conversion_report_pages()`) for memory efficiency
- Canonical JSON with `separators=(',', ':')` for deterministic signatures

## Commit Conventions

This project uses **Conventional Commits**:

```
<type>(<scope>): <description>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`

## CI/CD Pipeline

The CI pipeline (`.github/workflows/ci.yml`) runs on push/PR to `main`:

1. **Lint** - ruff check + format validation
2. **Security** - bandit + safety scanning
3. **Test** - pytest across Python 3.10-3.13 matrix; integration tests skip if no API credentials
4. **Type check** - mypy (non-blocking)
5. **Build** - package build + twine validation

All dependency installation in CI uses `uv pip install --system`.

## Test Markers

- `@pytest.mark.unit` - No external dependencies
- `@pytest.mark.integration` - Requires API credentials (SHOPEE_APP_ID, SHOPEE_APP_SECRET)
- `@pytest.mark.slow` - Long-running tests (deselect with `-m "not slow"`)

## Known Limitations

1. `generateShortLink` does not accept reserved words ("email", "canal", "utm") in sub-IDs
2. `conversionReport` only returns data from the last 3 months
3. `scrollId` expires after 30 seconds, limiting pagination speed for large reports
4. Official Shopee documentation is outdated - trust schemas discovered via introspection (see `docs/API_INTROSPECTION.md`)

## Key Documentation

- `docs/ARCHITECTURE.md` - System design and component interactions
- `docs/API_DOCUMENTACAO_COMPLETA.md` - Complete GraphQL schema documentation
- `docs/GUIA_COMPLETO.md` - Complete usage guide (Portuguese)
- `docs/OTIMIZACAO_DESEMPENHO.md` - Performance optimization strategies
- `CONTRIBUTING.md` - Contribution guidelines
- `ROADMAP.md` - Version planning and known issues
