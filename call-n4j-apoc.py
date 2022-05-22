import argparse
from pathlib import Path
import xml

from neo4j import GraphDatabase
import networkx as nx
import nxneo4j

from wsyntree import log
from wsyntree_collector.file.parse_file_treesitter import build_networkx_graph

def n4j_apoc_graphml_import(tx, filepath):
    # https://github.com/neo4j-contrib/neo4j-apoc-procedures/issues/2659
    tx.run(
        "CALL apoc.import.graphml(\"file://" + str(filepath) + "\", {readLabels: false})",
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", nargs="+", action="store", type=Path)
    parser.add_argument("--prefix", type=Path, default=Path("."))

    args = parser.parse_args()
    log.info(f"Total: {len(args.infile)}")

    driver = GraphDatabase.driver(uri="bolt://localhost:9787")

    for infile in args.infile:
        log.info(f"Importing {args.prefix / infile}")
        with driver.session() as session:
            session.write_transaction(n4j_apoc_graphml_import, args.prefix / infile)

    log.info(f"Total: {len(args.infile)}")

if __name__ == "__main__":
    main()
