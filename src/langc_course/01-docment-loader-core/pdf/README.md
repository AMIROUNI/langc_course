# Sample PDF

**Simple idea:** this folder holds the sample file used by the PDF loader
example.

| File | Used by |
| --- | --- |
| `Lettre_motivation_.pdf` | `exemple_pdf_laoder.py` in the parent folder. |

`PyPDFLoader` returns one `Document` per PDF page, so this file is a safe way to
try the loader without preparing your own PDF.

## Run the example

The script uses the relative path `./pdf/Lettre_motivation_.pdf`, so run it from
the parent folder:

```powershell
cd src/langc_course/01-docment-loader-core
uv run python exemple_pdf_laoder.py
```

Do not rename the PDF unless you also update the path in the script.

Back to [Step 1 - Document loaders](../README.md) or the
[course start](../../../../README.md).
