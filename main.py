import os
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


def get_module(file_content):
    return file_content.split()[1]


def trim(str):
    return str.strip().replace('"', '')


G = nx.DiGraph()

rootdir = '/Users/kalle/src/buffalo'
gofiles = []
for root, subdirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith(".go") and not file.endswith("_test.go"):
            gofiles.append(f'{root}/{file}')


for file in gofiles:
    f = open(file)

    fileContent = f.readlines()
    package = ''
    imports = []
    startIdx = -1
    endIdx = -1
    for idx, line in enumerate(fileContent):
        if line.startswith('package'):
            package = line.split()[1]
            if not G.has_node(package):
                G.add_node(package)
        if line.startswith('import'):
            if "(" not in line:
                imports.append(trim(line.split()[1].split('/')[-1]))
                break
            startIdx = idx
            continue
        if line.startswith(')'):
            endIdx = idx
            break

    if len(imports) < 1 and startIdx >= 0 and endIdx >= 0:
        imports = list(map(trim, fileContent[startIdx+1:endIdx]))

    for i in imports:
        if '/buffalo/' in i:
            pck = i.split('/')[-1]
            if not G.has_node(pck):
                G.add_node(pck)
            G.add_edge(package, pck)


nx.draw_networkx(G, with_labels=True, node_size=100)
g = Network(height='100%', width='100%', bgcolor='#222222',
            font_color='white', directed=True)
g.from_nx(G)
g.show("reconstruction.html")
