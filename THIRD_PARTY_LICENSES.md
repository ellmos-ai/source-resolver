# Third-Party Licenses & Dependency Inventory

## 1. Runtime Dependencies

`source-resolver` strictly enforces an audited **zero external runtime dependency** policy.
It operates entirely on the Python Standard Library without external third-party package requirements.

| Component | License | Origin | Operational Usage |
|-----------|---------|--------|-------------------|
| Python Standard Library (`dataclasses`, `enum`, `pathlib`, `json`, `typing`, `argparse`, `sys`) | Python Software Foundation License (PSFL-2.0) | Python Software Foundation | Core resolution ladder, store persistence, schema validation, CLI handling |

No third-party packages are installed, required, or imported for production runtime execution.

---

## 2. Zero-Copyleft & Data Sovereignty Guarantee

- **Zero-Copyleft Guarantee**: `source-resolver` is licensed under the permissive MIT License. Neither `source-resolver` nor any of its underlying standard library components impose viral copyleft obligations.
- **Data Sovereignty**: Skill configurations, source ladder definitions, resolution caches, and store files remain 100% owned by the host application and user.
- **Unprivileged RunAsInvoker Model**: The software operates entirely in unprivileged standard user space without requiring administrator rights, elevation, or system service daemons.

---

## 3. Development & Testing Dependencies

The following tools are used exclusively for offline development, automated contract verification, and code linting:

| Package | Version Range | License | Project URL |
|---------|---------------|---------|-------------|
| `pytest` | `>=8.0` | MIT License | https://github.com/pytest-dev/pytest |
| `ruff` | `>=0.4` | MIT / Apache-2.0 | https://github.com/astral-sh/ruff |

### pytest License (MIT License)

```text
The MIT License (MIT)

Copyright (c) 2004-2024 Holger Krekel and others

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### ruff License (MIT License / Apache 2.0)

```text
Copyright (c) 2023 Astral Software Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
