
from oscar import *

from pathlib import Path
import tempfile
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("commit", type=str)
    parser.add_argument("blob", type=str)
    parser.add_argument("filepath", type=str)

    args = parser.parse_args()

    commit = Commit(args.commit)
    blob = Blob(args.blob)
    tree = commit.tree

    # take file data and feed it into parser
    with tempfile.NamedTemporaryFile(mode='wb', prefix="supi-data", delete=False) as f:
        codepath = Path(f.name)
        print(f"Stored blob {blob} content to {codepath}, from source {args.filepath}")
        f.write(blob.data)

if __name__ == "__main__":
    main()

