import os
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


def get_module(file_content):
    return file_content.split()[1]


def trim(str):
    return str.strip().replace('"', '')


G = nx.Graph()

# rootdir = '/Users/kalle/src/devops-21'
rootdir = '/Users/kalle/src/buffalo'
#rootdir = '.'
gofiles = []
for root, subdirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith(".go") and not file.endswith("_test.go"):
            gofiles.append(f'{root}/{file}')

for file in gofiles:
    f = open(file)
    print(file)

    fileContent = f.readlines()
    # print(f'Module: {get_module(fileContent[0])}')
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
                imports.append(trim(line.split()[1]))
                break
            startIdx = idx
            continue
        if line.startswith(')'):
            endIdx = idx
            break

    if len(imports) < 1 and startIdx >= 0 and endIdx >= 0:
        imports = list(map(trim, fileContent[startIdx+1:endIdx]))

    for i in imports:
        if 'buffalo' in i:
            if not G.has_node(i):
                G.add_node(i)
            G.add_edge(package, i)

    print(list(filter(None, imports)))
    print(f'PACKAGE: {package}')
    print(startIdx)
    print(endIdx)
    print()

nx.draw_networkx(G, with_labels=True, node_size=100)
g = Network(height=900, width=1600)
g.from_nx(G)
g.show("ex.html")

# plt.show()
# plt.savefig('graph.png')
