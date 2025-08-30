import csv, chardet, os
from graphviz import Digraph

CSV_PATH = r"C:\Users\86178\Desktop\企业级次查询 25.06.csv"
PNG_PATH = os.path.join(os.path.dirname(CSV_PATH), "企业层级_平行.png") # 可在文件后选择所要更改的图片格式

#  配色
LEVEL_COLORS = [

    "#81D4FA",
]
# -------------------------

# 1. 读 CSV
with open(CSV_PATH, "rb") as f:
    enc = chardet.detect(f.read())["encoding"]
with open(CSV_PATH, encoding=enc) as f:
    rows = list(csv.reader(f))

# 2. 建图
dot = Digraph(
    name="企业层级",
    format="png",
    node_attr={"fontname": "SimSun", "fontsize": "12", "style": "filled"},
    graph_attr={
        "rankdir": "LR",
        "nodesep": "0.4",
        "ranksep": "1.2",
        "dpi": "600",
        "size": "40,25"
    }
)

root_id = "root"
dot.node(root_id, "企业层级图", shape="ellipse", fillcolor="#E0E0E0")

node_id = 0
def new_id():
    global node_id
    node_id += 1
    return f"n{node_id}"

# 3. 建树（平行子枝）
parents = [root_id]  # parents[level] = 当前层最后一个节点 id

for row in rows[1:]:
    for level, cell in enumerate(row):
        if cell and cell.strip():
            name = cell.strip()
            parent = parents[level]

            child = new_id()
            color = LEVEL_COLORS[level % len(LEVEL_COLORS)]
            dot.node(child, name, shape="box", fillcolor=color)

            dot.edge(parent, child)

            # 更新 parents
            if len(parents) <= level + 1:
                parents.append(child)
            else:
                parents[level + 1] = child

            parents = parents[: level + 2]

# 4. 渲染
dot.render(PNG_PATH, cleanup=True)
print("✅ 已生成：", PNG_PATH)