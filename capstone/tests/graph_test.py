import networkx as nx
import matplotlib.pyplot as plt
import json

content = "{\"summary\":\"Animal cells generate energy through cellular respiration in the mitochondria. The process involves three main steps: Glycolysis: Glucose is broken down in the cytoplasm, producing a small amount of energy and pyruvate molecules. Citric Acid Cycle (Krebs Cycle): Pyruvate enters the mitochondria, releasing energy and producing electron carriers. Oxidative Phosphorylation: Electron carriers transfer electrons through proteins in the inner mitochondrial membrane, generating a large amount of energy stored as ATP. ATP is the primary energy currency of the cell, powering various cellular functions.\", \"planning\":\"This information fits well in a flow chart because it outlines a sequential process with distinct steps, making it easier to visualize and understand the flow of energy production in animal cells. Here's how you could create a flow chart for cellular respiration: Start: Begin with a start symbol. Glycolysis: Use a process symbol to represent the breakdown of glucose in the cytoplasm. Pyruvate: Use an arrow to indicate the transition to the next step. Citric Acid Cycle (Krebs Cycle): Use another process symbol to show the entry of pyruvate into the mitochondria and the release of energy. Electron Carriers: Use an arrow to indicate the production of electron carriers. Oxidative Phosphorylation: Use a process symbol to represent the transfer of electrons through proteins in the inner mitochondrial membrane. ATP Production: Use an arrow to indicate the generation of ATP. End: Conclude with an end symbol. Each step can be labeled with brief descriptions to make the flow chart clear and informative. This visual representation helps in understanding the sequence and interconnections between the steps involved in cellular respiration.\", \"graph\":\"flowchart\", \"nodes\":[\"Start\", \"Glycosis\",\"Pyruvate\",\"Citric Acid Cycle (Krebs Cycle)\", \"Electron Carriers\", \"Oxidative Phosphorylation\", \"ATP Production\", \"End\"], \"edges\":[[\"Start\", \"Glycosis\"], [\"Glycosis\", \"Pyruvate\"], [\"Pyruvate\", \"Citric Acid Cycle (Krebs Cycle)\"], [\"Citric Acid Cycle (Krebs Cycle)\", \"Electron Carriers\"], [\"Electron Carriers\", \"Oxidative Phosphorylation\"], [\"Oxidative Phosphorylation\", \"ATP Production\"], [\"ATP Production\", \"End\"]]}"

content_json = json.loads(content)
print(content_json)
print(type(content_json))

G = nx.DiGraph()

for node in content_json["nodes"]:
    G.add_node(node)

for edge in content_json['edges']:
    G.add_edge(edge[0], edge[1])

pos = nx.circular_layout(G)

nx.draw(G, pos, with_labels=True, node_size=4000, node_color='skyblue', font_size=10, font_color='black', font_weight='bold', arrows=True)
plt.show()
