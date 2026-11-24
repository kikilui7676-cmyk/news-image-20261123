import hashlib
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    runpy.run_path(str(HERE / "render2.py"), run_name="__main__")
    data = (HERE / "entry.png").read_bytes()
    print(f"entry.png: {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
