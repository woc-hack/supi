import argparse
from pathlib import Path
import xml

from neo4j import GraphDatabase
import networkx as nx
import nxneo4j

from wsyntree import log
from wsyntree_collector.file.parse_file_treesitter import build_networkx_graph

def n4j_apoc_graphml_import(tx, filepath, commit):
    tx.run(
        ""
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", nargs="+", action="store", type=Path)
    parser.add_argument("--prefix", type=Path, default=Path("."))
    parser.add_argument("--outpath", type=Path, default=Path("data/merged"))

    args = parser.parse_args()

    driver = GraphDatabase.driver(uri="bolt://localhost:9787")

    for infile in args.infile:
        prefix = infile.stem
        print(f"Processing {args.prefix / infile} (prefix {prefix})")
        # insecure
        try:
            ingraph = nx.read_graphml(args.prefix / infile)
        except xml.etree.ElementTree.ParseError as e:
            log.error(e)
            continue
        nx.relabel_nodes(ingraph, lambda x: f"{prefix}_{x}", copy=False) # inplace
        nx.set_node_attributes(ingraph, prefix, "blob")
        types = nx.get_node_attributes(ingraph, "type")
        types = {k: f":{v}" if ingraph.nodes[k]['named']==True else ":unnamed" for k, v in types.items()}
        nx.set_node_attributes(ingraph, types, "labels")
        nx.write_graphml(ingraph, args.outpath / (infile.stem + ".graphml"), named_key_ids=True)

    log.info(f"Total: {len(args.infile)}")

if __name__ == "__main__":
    main()
