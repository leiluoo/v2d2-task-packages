"""Download and verify the selected task archives from the private GitHub release."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bucket", choices=("rl", "sft", "annealing", "all"), default="all")
    parser.add_argument("--output", type=Path, default=Path("data"))
    parser.add_argument("--no-extract", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifest.json").read_text())
    cache = args.output / "archives"
    cache.mkdir(parents=True, exist_ok=True)
    for asset in manifest["archives"]:
        if args.bucket != "all" and asset["bucket"] != args.bucket:
            continue
        path = cache / asset["name"]
        if not path.exists():
            subprocess.run([
                "gh", "release", "download", manifest["release_tag"],
                "--repo", "leiluoo/v2d2-task-packages", "--pattern", asset["name"],
                "--dir", str(cache),
            ], check=True)
        with path.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != asset["sha256"]:
            raise ValueError(f"Checksum mismatch: {path}; remove this file before retrying.")
        if path.stat().st_size != asset["bytes"]:
            raise ValueError(f"Size mismatch: {path}")
        if not args.no_extract:
            with tarfile.open(path, "r:gz") as archive:
                archive.extractall(args.output, filter="data")
        print(f"Verified {asset['name']}: {asset['task_count']} tasks", flush=True)


if __name__ == "__main__":
    main()
