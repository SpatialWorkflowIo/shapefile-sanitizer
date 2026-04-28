# Publishing to PyPI

This guide covers publishing `shapefile-sanitizer` to the Python Package Index (PyPI).

## Prerequisites

1. **PyPI Account**: Create one at https://pypi.org/account/register/
2. **Build tools**: Already included in `[dev]` extras

## Step 1: Create PyPI API Token

1. Go to https://pypi.org/manage/account/
2. Scroll to **API tokens**
3. Click **Add API token**
4. Name it `shapefile-sanitizer`
5. Set scope to **Entire account** (or just this project)
6. Copy the token (starts with `pypi-`)

## Step 2: Configure `~/.pypirc` (optional but recommended)

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Or use environment variable (one-liner):

```bash
export TWINE_PASSWORD="pypi-YOUR_TOKEN_HERE"
```

## Step 3: Build and Publish

### Install build tools (if not already installed)

```bash
pip install build twine
```

### Build the package

```bash
python -m build
```

This creates `dist/` with both source distribution (`.tar.gz`) and wheel (`.whl`).

### Upload to PyPI

```bash
python -m twine upload dist/*
```

You'll be prompted for username (`__token__`) and password (your API token).

### Verify

After 1-2 minutes:

```bash
pip install shapefile-sanitizer
```

Or check: https://pypi.org/project/shapefile-sanitizer/

## Step 4 (Future): Update Version & Re-publish

1. Edit `pyproject.toml` — bump `version` (e.g., `0.1.0` → `0.2.0`)
2. Rebuild:
   ```bash
   rm -rf dist/  # Clean old builds
   python -m build
   ```
3. Re-upload:
   ```bash
   python -m twine upload dist/*
   ```

## Troubleshooting

### "Repository not found"
- Verify PyPI token is valid (not expired)
- Check `~/.pypirc` is readable: `cat ~/.pypirc`

### "File already exists"
- PyPI doesn't allow overwriting versions
- Must bump version in `pyproject.toml` and rebuild

### "Forbidden: …has been blocked"
- PyPI may have security holds on new accounts
- Wait a few days or contact PyPI support

## GitHub Actions (CI/CD Alternative)

To auto-publish on release, create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install build twine
      - run: python -m build
      - run: python -m twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

Then in GitHub repo settings, add secret `PYPI_API_TOKEN` with your PyPI token.

---

For more info: https://packaging.python.org/tutorials/packaging-projects/

