# news-image-20261123 — broadsheet 1600x2240, 23 November 2026, 43 cerita.
# Entrypoint tipis: mengeksekusi render2.py sebagai __main__ agar ia menulis
# entry.png di samping file ini. Semua layout dan gambar hidup di render2.py.

from pathlib import Path as _Pth
import runpy as _rpy


def _jalankan_broadsheet_23_november_2026():
    _renderer = _Pth(__file__).resolve().parent / "render2.py"
    _rpy.run_path(str(_renderer), run_name="__main__")


_dijalankan_langsung = __name__ == "__main__"
if _dijalankan_langsung:
    _jalankan_broadsheet_23_november_2026()
