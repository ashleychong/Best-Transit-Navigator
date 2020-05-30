import plotly.graph_objects as go
# fig = go.Figure(
#     data=[go.Bar(y=[2, 1, 3])],
#     layout_title_text="A Figure Displayed with fig.show()"
# )

trace0 = go.Bar(
    x=["Apples", "Cherries", "Honeydew", "Oranges", "Bananas"],
    y=["5", "10", "3", "10", "5"],
    name="Figure 1"
)

fig = go.Figure()
fig.add_trace(trace0)
fig.show()
