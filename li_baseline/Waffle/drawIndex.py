import plotly.graph_objects as go

height = 0
nodes = []
with open("Index.csv") as f:
    for i, line in enumerate(f):
        if int(line.split(",")[0]) == height:
            nodes.append(
                (
                    float(line.split(",")[2]),
                    float(line.split(",")[3]),
                    float(line.split(",")[4]),
                    float(line.split(",")[5]),
                )
            )

fig = go.Figure()

# Set axes properties
fig.update_xaxes(
    range=[-182, 182],
    showgrid=False,
    zeroline=False,
    mirror=True,
    # ticks="outside",
    showticklabels=False,
    showline=False,
    linecolor="black",
)
fig.update_yaxes(
    range=[-91, 91],
    showgrid=False,
    zeroline=False,
    mirror=True,
    # ticks="outside",
    showticklabels=False,
    showline=False,
    linecolor="black",
)

perimeter = 0

# Add shapes
for n in nodes:
    fig.add_trace(
        go.Scatter(
            mode="lines",
            x=[n[0], n[0], n[2], n[2], n[0]],
            y=[n[1], n[3], n[3], n[1], n[1]],
            line=dict(color="black", width=0.75),
        )
    )
    perimeter += 2 * ((n[2] - n[0]) + (n[3] - n[1]))

numNodes = len(nodes)
avgLen = perimeter / numNodes
print(
    f"Total Number of Nodes: {numNodes}\nAverage Perimeter: {avgLen:.2f}\n"
)

# fig.update_shapes(dict(xref='x', yref='y', line=dict(color="black")))
fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(l=0, r=0, t=0, b=0),
    height=720,
    width=1440,
)
fig.write_image(file="Index.png")
