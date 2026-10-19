import ast
from collections import Counter

import pandas as pd


class Node:
    def __init__(self, item):
        self.item = item
        self.count = 0
        self.children = {}


class SkillTree:
    """Prefix tree over pre-ordered lists: [dev type, skill, skill, ...]."""

    def __init__(self, transactions):
        self.root = Node(None)
        self.items = set()
        for t in transactions:
            if isinstance(t, str):               # list saved in a CSV comes back as text
                t = ast.literal_eval(t)
            node = self.root
            for item in t:
                node = node.children.setdefault(item, Node(item))
                node.count += 1
                self.items.add(item)

    def next_nodes(self, dev, skills, top_n=10):
        """Rebuild every person's full list in the dev type's branch. If it contains
        all of the user's skills, count each of its other skills (before or after).
        Returns ([(skill, likelihood %), ...], total), where total is the number of
        people in that dev type who have all of the user's skills, and likelihood is
        the share of those people who also have the skill."""
        skills = set(skills) & self.items        # ignore unknown skills
        start = self.root.children.get(dev)
        if start is None:
            return [], 0
        scores = Counter()
        total = 0
        stack = [(start, [])]
        while stack:
            node, path = stack.pop()
            path = path + [node.item]
            # how many people's lists end exactly at this node
            ends = node.count - sum(c.count for c in node.children.values())
            if ends and skills <= set(path):
                total += ends
                for item in path[1:]:            # path[0] is the dev type
                    if item not in skills:
                        scores[item] += ends
            for child in node.children.values():
                stack.append((child, path))
        if total == 0:
            return [], 0
        return [(s, c / total * 100) for s, c in scores.most_common(top_n)], total


df = pd.read_csv("FinalDataset.csv")
tree_work = SkillTree(df["workwithcolumn"])
tree_total = SkillTree(df["work_wantcolumn"])