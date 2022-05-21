
from oscar import *

from pathlib import Path
import tempfile
import argparse

from write_to_n4j import *


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("commit", type=str)
    parser.add_argument("blob", type=str)
    parser.add_argument("filepath", type=str)
    parser.add_argument("-l", "--lang", help="Language parser to use", default="cpp")

    args = parser.parse_args()

    lang = TreeSitterAutoBuiltLanguage(args.lang)
    commit = Commit(args.commit)
    blob = Blob(args.blob)
    tree = commit.tree

    # take file data and feed it into parser
    with tempfile.NamedTemporaryFile(mode='wb', prefix="supi-data", delete=False) as f:
        codepath = Path(f.name)
        print(f"Stored blob {blob} content to {codepath}, from source {args.filepath}")
        f.write(blob.data)
    
    driver = GraphDatabase.driver(uri="bolt://localhost")
    G = nx.DiGraph(driver)

    _, code_node = add_to_graph(
        lang, codepath, G, start_node
    )

    print(f"Done adding, first node: {code_node}")

if __name__ == "__main__":
    main()

