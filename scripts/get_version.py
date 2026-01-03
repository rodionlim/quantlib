from __future__ import annotations

import ast
from pathlib import Path


def get_version_from_setup_py(setup_py: Path) -> str:
    tree = ast.parse(setup_py.read_text(encoding="utf-8"), filename=str(setup_py))

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "setup":
            for kw in node.keywords:
                if kw.arg == "version" and isinstance(kw.value, ast.Constant):
                    if isinstance(kw.value.value, str):
                        return kw.value.value

    raise RuntimeError("Could not find a string literal version=... in setup.py")


def main() -> None:
    setup_py = Path(__file__).resolve().parents[1] / "setup.py"
    print(get_version_from_setup_py(setup_py))


if __name__ == "__main__":
    main()
