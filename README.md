[Uploading HierViz-Enterprise.md…]()
# HierViz-Enterprise  
> 读一份「企业级次」CSV，自动生成高清横向层级关系图（Graphviz）

---

## 🚀 1 分钟跑起来
```bash
git clone git@github.com:Seventh331/-Xmind-.git
cd -Xmind-
pip install -r requirements.txt    # 若已装可跳过
python HierViz.py
```

## 📦 依赖列表

| 库           | 安装命令               | 版本示例 | 作用说明                                                     |
| ------------ | ---------------------- | -------- | ------------------------------------------------------------ |
| **graphviz** | `pip install graphviz` | ≥0.20    | Python 接口：把节点/边对象渲染成 `.png / .pdf` 等文件        |
| **chardet**  | `pip install chardet`  | ≥5.0     | 编码嗅探：自动识别 CSV 文件编码（GBK / UTF-8 / ISO-8859-1…） |
| **csv**      | 内置，无需安装         | —        | 标准库：逐行读取 CSV 文件，支持分隔符、引号、转义            |

> 还需在系统里安装 **Graphviz 可执行文件** 才能生成图片  
> - macOS: `brew install graphviz`  
>
> - Windows: 下载 [Graphviz 安装包](https://graphviz.org/download/) 并把 `bin` 目录加入 PATH
>
> - 下面用「文件长什么样 → 代码怎么读 → 怎么变树 → 怎么画图」4 个步骤，把整件事一次讲透。  
>   你直接复制下面的 `README_detail.md` 到 Typora 即可用。
>
>   ---
>
>   # HierViz 逐行超详细讲解
>
>   ---
>
>   ## 1️⃣ 原始 CSV 到底长什么样？
>
>   把 `企业级次查询 25.06.csv` 用 Excel / Numbers 打开，会看到 5 列，分别是：
>
>   | 一级企业 | 二级企业 | 三级企业 | 四级企业(88户) | 五级企业(3户) |
>   | -------- | -------- | -------- | -------------- | ------------- |
>   | 宏达集团 |          |          |                |               |
>   |          | 宏达投资 |          |                |               |
>   |          |          | 宏达地产 |                |               |
>   |          |          |          | 宏达物业       |               |
>   |          |          |          |                | 宏达保安      |
>
>   **规律：**  
>   - **每行就是一条“枝干”**  
>   - **单元格为空 → 说明这一级没有节点**  
>   - **每出现一次非空单元格 → 就生出一个新节点**  
>   - **整份文件的所有行拼在一起，就得到一片森林**
>
>   ---
>
>   ## 2️⃣ Python 读取文件：解决乱码 & 拿到二维列表
>
>   ```python
>   with open(CSV_PATH, "rb") as f:
>       enc = chardet.detect(f.read())["encoding"]   # 1️⃣ 先探测编码
>   with open(CSV_PATH, encoding=enc) as f:
>       rows = list(csv.reader(f))                   # 2️⃣ 再读成二维 list
>   ```
>
>   - **chardet**：防止 GBK/UTF-8/ANSI 乱码。  
>   - **csv.reader**：把每行变成 `['一级','二级',...]` 这样的 Python 列表。
>
>   读完以后 `rows[0]` 是表头，**真正数据从 `rows[1:]` 开始**。
>
>   ---
>
>   ## 3️⃣ 把二维列表变“树”的核心算法
>
>   算法只用 1 个变量：`parents[level] = 当前层最后一个节点 id`
>
>   | 步骤 | 动作                   | 例子                              |
>   | ---- | ---------------------- | --------------------------------- |
>   | ①    | 初始化                 | `parents = [root]`                |
>   | ②    | 遍历每一行的每一格     |                                   |
>   | ③    | 如果格子非空，新建节点 | `child = n1`                      |
>   | ④    | 连到父节点             | `dot.edge(parents[level], child)` |
>   | ⑤    | 更新 parents 数组      | `parents[level+1] = child`        |
>
>   代码对应片段（已加行号）：
>
>   ```python
>   parents = [root_id]                  # 43 行
>   for row in rows[1:]:                 # 45 行
>       for level, cell in enumerate(row):
>           if cell and cell.strip():    # 48 行：跳过空白格
>               name = cell.strip()
>               parent = parents[level]  # 找到父节点 id
>               child  = new_id()        # 生成新节点 id
>               dot.node(child, name, ...)   # 创建节点
>               dot.edge(parent, child)      # 画边
>               # 更新 parents[level+1] 为当前节点 id
>               if len(parents) <= level + 1:
>                   parents.append(child)
>               else:
>                   parents[level + 1] = child
>               parents = parents[:level + 2]  # 截断，防止同级串枝
>   ```
>
>   ---
>
>   ## 4️⃣ 生成高清 PNG 的 3 个关键参数
>
>   ```python
>   dot = Digraph(
>       format="png",
>       graph_attr={
>           "rankdir": "LR",   # 横向树
>           "nodesep": "0.4",  # 节点左右间距
>           "ranksep": "1.2",  # 层与层间距
>           "dpi": "600",      # 分辨率
>           "size": "40,25"    # 画布宽×高（英寸）
>       }
>   )
>   ```
>
>   - **rankdir=LR**：横向布局，企业级次从左到右展开。  
>   - **dpi=600**：A4 打印也清晰。  
>   - **size=40,25**：防止节点过多时被压缩。
>
>   ---
>
>   ## 5️⃣ 运行结果
>
>   终端打印：
>
>   ```
>   ✅ 已生成：/Users/…/企业级次_平行.png
>   ```
>
>   用任意图片查看器打开，会看到：
>
>   ```
>   宏达集团 → 宏达投资 → 宏达地产 → 宏达物业 → 宏达保安
>   ```
>
>   每家企业都是一个彩色矩形，层级一目了然。
>
>   ---
>
>   ## 6️⃣ 二次开发 Checklist
>
>   | 想改什么     | 改哪里                                     |
>   | ------------ | ------------------------------------------ |
>   | 纵向树       | `"rankdir": "TB"`                          |
>   | 更多层级颜色 | 把 `LEVEL_COLORS` 列表加长                 |
>   | 输出 PDF/SVG | `format="pdf"` 或 `"svg"`                  |
>   | 支持 Excel   | 把 `csv.reader` 换成 `pandas.read_excel()` |
>
>   ---
>
>   至此，文件 → 二维表 → 树 → 高清图 整个链路全部打通。
