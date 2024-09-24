"""
Draft program for capstone to use OpenAI to programmatically generate diagrams from student notes

Description:
Intakes notes and uses prompt engineering to get back a formatted response from GPT to programmatically generate diagrams based on the type of information provided.

Author: Andrew Ge
Email: andrew.ge677@myci.csuci.edu 
Date: September 24 2024

Usage: run with your own OpenAI key in a file in active directory called 'key.txt', then paste in notes when prompted. Notes work best with all attributes like dates and percentages explicitly written (don't leave GPT to calculate a remaining percentage, date, etc.). 

Notes: in progress. 

Upcoming Changes: 
- generate more types of diagrams
- use the schemdraw library for better flowcharts
"""

import json
import numpy as np
from openai import OpenAI
import networkx as nx
import matplotlib.pyplot as plt

f = open("key.txt", "r")
OPENAI_KEY = f.read()
client = OpenAI(api_key=OPENAI_KEY)
f.close()

with open("diagram_generator\\prompt.json", "r") as f:
    conversation = json.load(f)

input_notes = input("Enter notes:\n")
conversation['messages'].append({
    "role": "user",
    "content": input_notes
})

# print(conversation)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=conversation['messages'],
    response_format={"type": "json_object"}
)

data = completion.model_dump_json()
json_data = completion.to_json()
# print(data)

chat_completion_dict = json.loads(json_data)
# print(chat_completion_dict)

response = json.loads(chat_completion_dict["choices"][0]["message"]["content"])

print("\n\n\n")

for key, value in response.items():
    print(f"{key}: {value}")

graph_type = response['graph']

if graph_type == "flowchart":
    nodes = response['nodes']
    edges = response['edges']

    flowchart = nx.DiGraph()
    for node in nodes:
        flowchart.add_node(node)
    for edge in edges:
        flowchart.add_edge(edge[0], edge[1])
    pos = nx.circular_layout(flowchart)
    nx.draw(flowchart, pos, with_labels=True, node_size=4000, node_color='skyblue',
            font_size=10, font_color='black', font_weight='bold', arrows=True)
    plt.show()

elif graph_type == "timeline":
    events = response["events"]
    dates = []
    labels = []
    for date, label in events:
        dates.append(int(date))
        labels.append(label)
    print(dates)
    fig, ax = plt.subplots(figsize=(15, 4), constrained_layout=True)
    _ = ax.set_ylim(-2, 1.75)
    _ = ax.set_xlim(min(dates), max(dates))
    _ = ax.axhline(0, xmin=0.05, xmax=0.95, c='deeppink', zorder=1)
    _ = ax.scatter(dates, np.zeros(len(dates)), s=120, c='palevioletred', zorder=2)
    _ = ax.scatter(dates, np.zeros(len(dates)), s=30, c='darkmagenta', zorder=3)
    label_offsets = np.zeros(len(dates))
    label_offsets[::2] = 0.35
    label_offsets[1::2] = -0.7
    for i, (l, d) in enumerate(zip(labels, dates)):
        _ = ax.text(d, label_offsets[i], f"{d}: {l}", ha='center', fontfamily='serif', fontweight='bold', color='royalblue',fontsize=12)
    stems = np.zeros(len(dates))
    stems[::2] = 0.3
    stems[1::2] = -0.3   
    markerline, stemline, baseline = ax.stem(dates, stems)
    _ = plt.setp(markerline, marker=',', color='darkmagenta')
    _ = plt.setp(stemline, color='darkmagenta')
    # hide lines around chart
    for spine in ["left", "top", "right", "bottom"]:
        _ = ax.spines[spine].set_visible(False)
    # hide tick labels
    _ = ax.set_xticks([])
    _ = ax.set_yticks([])

    # _ = ax.set_title('Andrew\'s Timeline', fontweight="bold", fontfamily='serif', fontsize=16, 
    #                 color='royalblue')
    plt.show()

elif graph_type == "pie chart":
    sections = response["percentages"]
    fig, ax = plt.subplots()
    percentages = []
    labels = []
    for percentage, label in sections:
        percentages.append(percentage)
        labels.append(label)
    ax.pie(percentages, labels=labels, autopct='%1.1f%%')
    plt.show()
