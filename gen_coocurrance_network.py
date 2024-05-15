from collections import Counter
from functools import reduce
from itertools import combinations
from typing import Iterable

import pandas as pd
from pyvis.network import Network


def build_network(categories: Iterable[list[str]]) -> Network:
    category_occurrance = Counter(reduce(lambda i, j: i + j, categories))
    category_combinations = [list(combinations(cat, r=2)) for cat in categories]
    category_combinations = list(reduce(lambda i, j: i + j, category_combinations))
    combination_coocurrance = Counter([i for i in category_combinations if len(i)])

    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", filter_menu=True)

    for (edge_1, edge_2), count in combination_coocurrance.items():
        net.add_node(edge_1, edge_1, title=edge_1, value=category_occurrance[edge_1])
        net.add_node(edge_2, edge_2, title=edge_2, value=category_occurrance[edge_2])
        net.add_edge(edge_1, edge_2, value=count)

    return net


if __name__ == "__main__":
    df = pd.read_csv("database.csv")
    categories = [cat.split(", ") for cat in df["Category"] if not pd.isna(cat)]
    net = build_network(categories)
    net.show("co-occurrance-network.html", notebook=False)
