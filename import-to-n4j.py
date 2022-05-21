
from oscar import *

from pathlib import Path
import tempfile
import argparse

from wsyntree_collector.file.parse_file_treesitter import build_networkx_graph
from write_to_n4j import *
import networkx as nx


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
    
    outfile = Path(f"data/{args.blob}.graphml")

    G = build_networkx_graph(lang, codepath, include_text=True)
    nx.write_graphml(G, outfile)

    print(f"File {outfile} written.")

if __name__ == "__main__":
    main()

