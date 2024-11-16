"""
Draft program for capstone to use OpenAI to programmatically generate diagrams from student notes

Description:
Intakes notes and uses prompt engineering to get back a formatted response from GPT to 
programmatically generate diagrams based on the type of information provided.

Author: Andrew Ge
Email: andrew.ge677@myci.csuci.edu 
Date: September 24 2024

Usage: run with your own OpenAI key in a file in active directory called 'key.txt', 
then paste in notes when prompted. 
Notes work best with all attributes like dates and percentages explicitly written 
(don't leave GPT to calculate a remaining percentage, date, etc.). 

Generates the following types of graphs: flowchart, timeline, piechart, barchart, table

"""

import json
import re
import numpy as np
from openai import OpenAI
import matplotlib.pyplot as plt
import pandas as pd
from blockdiag import parser, builder, drawer

DATETIME_PATTERNS = [
    r'^\d{4}$',
    r'^\d{4}-\d{1,2}$',
    r'^\d{4}-\d{1,2}-\d{1,2}$'
]

PROMPT_PATH = "capstone\\diagram_generator\\prompt.json"

with open("key.txt", "r", encoding="utf-8") as f:
    OPENAI_KEY = f.read()
    client = OpenAI(api_key=OPENAI_KEY)

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    conversation = json.load(f)

input_notes = input("Enter notes:\n")
conversation['messages'].append({
    "role": "user",
    "content": input_notes
})

COMPLETION = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=conversation['messages'],
    response_format={"type": "json_object"}
)

data = COMPLETION.model_dump_json()
json_data = COMPLETION.to_json()

chat_completion_dict = json.loads(json_data)

response = json.loads(chat_completion_dict["choices"][0]["message"]["content"])

print("\n\n\n")

for key, value in response.items():
    print(f"{key}: {value}")

graph_type = response['graph']

if graph_type == "flowchart":
    nodes = response['nodes']
    edges = response['edges']
    diagram_code = "blockdiag {\n"
    for edge in edges:
        diagram_code += f"'{edge[0]}' -> '{edge[1]}';\n"
    diagram_code += "}"
    tree = parser.parse_string(diagram_code)
    diagram = builder.ScreenNodeBuilder.build(tree)
    draw = drawer.DiagramDraw('PNG', diagram, filename="basic_diagram.png")
    draw.draw()
    print(draw)
    draw.save()

elif graph_type == "timeline":
    events = response["events"]
    dates = []
    labels = []
    for date, label in events:
        if re.match(DATETIME_PATTERNS[0], date):
            dates.append(float(date))
            labels.append(f"{date}: {label}")
        elif re.match(DATETIME_PATTERNS[1], date):
            dates.append(float(date[0:4]) + float(date[5:7])/12.0)
            labels.append(f"{date[0:4]}-{date[5:7]}: {label}")
        elif re.match(DATETIME_PATTERNS[2], date):
            dates.append(float(date[0:4]) + float(date[5:7]
                                                  )/12.0 + float(date[8:10])/365.0)
            labels.append(f"{date[0:4]}-{date[5:7]}-{date[8:10]}: {label}")
        else:
            print(f"Timeline graph error: unexpected date format: {date}")
    fig, ax = plt.subplots(figsize=(15, 4), constrained_layout=True)
    _ = ax.set_ylim(-2, 1.75)
    _ = ax.set_xlim(min(dates), max(dates))
    _ = ax.axhline(0, xmin=0.05, xmax=0.95, c='deeppink', zorder=1)
    _ = ax.scatter(dates, np.zeros(len(dates)),
                   s=120, c='palevioletred', zorder=2)
    _ = ax.scatter(dates, np.zeros(len(dates)),
                   s=30, c='darkmagenta', zorder=3)
    label_offsets = np.zeros(len(dates))
    label_offsets[::2] = 0.35
    label_offsets[1::2] = -0.7
    for i, (l, d) in enumerate(zip(labels, dates)):
        _ = ax.text(d, label_offsets[i], f"{l}", ha='center', fontfamily='serif', fontweight='bold', color='royalblue', fontsize=12)
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

elif graph_type == "bar chart":
    bars = response["bars"]
    values = [i[0] for i in bars]
    categories = [i[1] for i in bars]
    plt.bar(categories, values)
    plt.xlabel(response["x Axis"])
    plt.ylabel(response["y Axis"])
    plt.show()
    plt.savefig('bar_chart.png')

elif graph_type == "table":
    columns = response["columns"]
    df = {}
    for item in columns:
        df.update(item)
    df = pd.DataFrame(df)
    print(df)
    # Create a matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figsize parameter for more text
    ax.axis('tight')
    ax.axis('off')
    # Create a table with adjusted cell dimensions
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    # Set font size for the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    # Adjust column widths
    table.auto_set_column_width(col=list(range(len(df.columns))))
    # Save the table as a PNG file
    plt.savefig('table.png', bbox_inches='tight', pad_inches=0.1)
    plt.close()

else:
    print(f"Error unknown graph type provided by GPT: {graph_type}")