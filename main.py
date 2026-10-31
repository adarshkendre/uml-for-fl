"""
main.py
=======
Converts all PlantUML (.puml) files in diagram-source-code/uml/
to PNG images saved in output/images/.

Two rendering modes (auto-detected):
  1. Local jar  – java -jar plantuml.jar   (offline, best quality)
  2. Server     – public PlantUML server   (internet, no install needed)

Usage
-----
  python main.py                          # auto-detect
  python main.py --server                 # force server mode
  python main.py --jar plantuml.jar       # force local jar
  python main.py --format svg             # change output format
  python main.py --src path/to/puml       # custom source folder
  python main.py --out path/to/output     # custom output folder
"""

import argparse
import shutil
import subprocess
import sys
import urllib.request
import zlib
from pathlib import Path

# ── Defaults ──────────────────────────────────────────────────────────────────
DEFAULT_SRC = Path(__file__).parent / "diagram-source-code" / "uml"
DEFAULT_OUT = Path(__file__).parent / "output" / "images"
DEFAULT_JAR = ""          # set to r"C:\tools\plantuml.jar" if desired
DEFAULT_FMT = "png"
SERVER_URL  = "http://www.plantuml.com/plantuml"
# ─────────────────────────────────────────────────────────────────────────────


# ── PlantUML URL encoding (server mode) ──────────────────────────────────────
_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def _enc6(b: int) -> str:
    return _CHARS[b & 0x3F]

def _enc3(b1: int, b2: int, b3: int) -> str:
    return (
        _enc6(b1 >> 2)
        + _enc6(((b1 & 0x3) << 4) | (b2 >> 4))
        + _enc6(((b2 & 0xF) << 2) | (b3 >> 6))
        + _enc6(b3 & 0x3F)
    )

def puml_encode(text: str) -> str:
    """Encode PlantUML source for embedding in a server URL."""
    data = zlib.compress(text.encode("utf-8"), 9)
    out, i = [], 0
    while i < len(data):
        b1 = data[i]
        b2 = data[i + 1] if i + 1 < len(data) else 0
        b3 = data[i + 2] if i + 2 < len(data) else 0
        out.append(_enc3(b1, b2, b3))
        i += 3
    return "".join(out)
# ─────────────────────────────────────────────────────────────────────────────


def banner(label: str) -> None:
    print(f"\n{'='*55}\n  {label}\n{'='*55}")


def convert_jar(jar: str, files: list, out: Path, fmt: str) -> dict:
    java = shutil.which("java")
    if not java:
        print("[ERROR] Java not found on PATH. Install JRE 8+ from https://adoptium.net/")
        sys.exit(1)

    results = {}
    for f in files:
        print(f"  [{f.name}]", end=" ", flush=True)
        cmd = [java, "-jar", jar, f"-t{fmt}", "-o", str(out.resolve()), str(f.resolve())]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if r.returncode == 0:
                results[f.name] = True
                print("OK")
            else:
                results[f.name] = False
                print(f"FAILED\n      {r.stderr.strip()}")
        except subprocess.TimeoutExpired:
            results[f.name] = False
            print("TIMEOUT")
        except Exception as e:
            results[f.name] = False
            print(f"ERROR: {e}")
    return results


def convert_server(files: list, out: Path, fmt: str) -> dict:
    if fmt not in ("png", "svg", "txt"):
        print(f"[WARN] Server supports png/svg/txt only – switching to png.")
        fmt = "png"

    results = {}
    for f in files:
        dest = out / f"{f.stem}.{fmt}"
        print(f"  [{f.name}]", end=" ", flush=True)
        try:
            src     = f.read_text(encoding="utf-8")
            encoded = puml_encode(src)
            url     = f"{SERVER_URL}/{fmt}/{encoded}"
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = resp.read()
            dest.write_bytes(data)
            results[f.name] = True
            print(f"OK  ({len(data):,} bytes)  →  {dest.name}")
        except Exception as e:
            results[f.name] = False
            print(f"ERROR: {e}")
    return results


def print_summary(results: dict) -> None:
    ok  = [k for k, v in results.items() if v]
    err = [k for k, v in results.items() if not v]
    print(f"\n  Succeeded : {len(ok)}")
    print(f"  Failed    : {len(err)}")
    if err:
        print("  Failed files:")
        for name in err:
            print(f"    - {name}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Convert PlantUML files to images.")
    ap.add_argument("--src",    default=str(DEFAULT_SRC), help="Source folder with .puml files")
    ap.add_argument("--out",    default=str(DEFAULT_OUT), help="Output folder for images")
    ap.add_argument("--jar",    default=DEFAULT_JAR,      help="Path to plantuml.jar")
    ap.add_argument("--server", action="store_true",      help="Force public PlantUML server")
    ap.add_argument("--format", default=DEFAULT_FMT,
                    choices=["png", "svg", "eps", "pdf", "txt"],
                    help="Output format (default: png)")
    args = ap.parse_args()

    src_dir = Path(args.src)
    out_dir = Path(args.out)

    puml_files = sorted(src_dir.glob("*.puml"))
    if not puml_files:
        print(f"[ERROR] No .puml files found in: {src_dir}")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    banner("PlantUML → Image Converter")
    print(f"  Source  : {src_dir.resolve()}")
    print(f"  Output  : {out_dir.resolve()}")
    print(f"  Format  : {args.format}")
    print(f"  Diagrams: {len(puml_files)} file(s) found")

    # ── Decide rendering mode ────────────────────────────────────────────────
    if args.server:
        mode = "server"
    elif args.jar and Path(args.jar).is_file():
        mode, jar = "jar", args.jar
    elif DEFAULT_JAR and Path(DEFAULT_JAR).is_file():
        mode, jar = "jar", DEFAULT_JAR
    else:
        local_jar = Path(__file__).parent / "plantuml.jar"
        if local_jar.is_file():
            mode, jar = "jar", str(local_jar)
        else:
            mode = "server"
            print("\n  [INFO] plantuml.jar not found → using public PlantUML server.")
            print("         For offline use: download plantuml.jar and place next to main.py")
    # ────────────────────────────────────────────────────────────────────────

    print(f"  Mode    : {'Local jar (' + jar + ')' if mode == 'jar' else 'PlantUML server (' + SERVER_URL + ')'}\n")

    if mode == "jar":
        results = convert_jar(jar, puml_files, out_dir, args.format)
    else:
        results = convert_server(puml_files, out_dir, args.format)

    banner("Summary")
    print_summary(results)
    print(f"\n  Images saved to:\n  {out_dir.resolve()}\n")


if __name__ == "__main__":
    main()
