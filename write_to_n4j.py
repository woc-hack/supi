
from itertools import chain
from pathlib import Path

# import networkx as nx
import nxneo4j as nx
from neo4j import GraphDatabase

from wsyntree import log
from wsyntree.utils import dotdict
from wsyntree.wrap_tree_sitter import TreeSitterAutoBuiltLanguage, TreeSitterCursorIterator


def add_to_graph(
        lang: TreeSitterAutoBuiltLanguage,
        file: Path,
        G: 'nx.DiGraph',
        start_node,
        only_named_nodes: bool = False,
        include_text: bool = False,
    ):
    tree = lang.parse_file(file)
    cur = tree.walk()

    if only_named_nodes:
        cursor = TreeSitterCursorIterator(cur, nodefilter=lambda x: x.is_named)
    else:
        cursor = TreeSitterCursorIterator(cur)

    # G = nx.DiGraph(lang=lang.lang)

    parent_stack = []
    ts_id_to_preorder = {}

    root = cursor.peek()
    # ts_id_to_preorder[root.id] = 0
    first_node = None

    for cur_node in chain([root], cursor):
        preorder = cursor._preorder

        nn = dotdict({
            # preorder=preorder,
            "id": cur_node.id,
            "named": cur_node.is_named,
            "type": cur_node.type,
        })
        (nn.x1,nn.y1) = cur_node.start_point
        (nn.x2,nn.y2) = cur_node.end_point

        ts_id_to_preorder[cur_node.id] = preorder
        parent_order = parent_stack[-1] if parent_stack else None

        if include_text:
            raise NotImplementedError(f"text decoding TODO")

        log.debug(f"adding node {preorder}: {nn}")
        # insert node and it's data
        node = G.add_node(preorder, **nn)
        if not first_node:
            first_node = node

        # add the edge
        if cur_node.parent is not None:
            log.debug(f"connecting node {preorder}, to id {cur_node.parent.id}")
            G.add_edge(
                ts_id_to_preorder[cur_node.parent.id],
                preorder
            )

    return (G, first_node)
