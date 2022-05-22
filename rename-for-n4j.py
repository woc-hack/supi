import argparse
from pathlib import Path
import xml

from neo4j import GraphDatabase
import networkx as nx
import nxneo4j

from wsyntree import log
from wsyntree_collector.file.parse_file_treesitter import build_networkx_graph

from pebble import ProcessPool
from multiprocessing import cpu_count
from concurrent.futures import TimeoutError


def modify_graphml(farg):
    infile, args = farg
    log.info(f"Processing {args.prefix / infile}")
    # insecure
    try:
        ingraph = nx.read_graphml(args.prefix / infile)
    except xml.etree.ElementTree.ParseError as e:
        log.error(e)
        return "skipped"
    nx.relabel_nodes(ingraph, lambda x: f"{prefix}-{x}", copy=False) # inplace
    nx.set_node_attributes(ingraph, infile.stem, "blob")
    types = nx.get_node_attributes(ingraph, "type")
    types = {k: f":{v}" if ingraph.nodes[k]['named']==True else ":unnamed" for k, v in list(types.items())}
    nx.set_node_attributes(ingraph, types, "labels")
    nx.write_graphml(ingraph, args.outpath / (infile.stem + ".graphml"), named_key_ids=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", nargs="+", action="store", type=Path)
    parser.add_argument("--prefix", type=Path, default=Path("."))
    parser.add_argument("--outpath", type=Path, default=Path("data/merged"))

    args = parser.parse_args()

    with ProcessPool(max_workers=cpu_count()) as pool:
        future = pool.map(
                modify_graphml,
                [ (infile, args) for infile in args.infile],
                chunksize=64,
                timeout=300
        )

        results = future.result()

    for r in results:
        if isinstance(r, Exception):
            log.err(r)
            raise r

    log.info(f"Total: {len(list(results))}")

if __name__ == "__main__":
    main()
