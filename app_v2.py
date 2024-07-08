# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
url = "https://raw.githubusercontent.com/NelbaBarreto/programacion-ciencias-datos/main/data/dinosaurs_dataset.csv"
df = pd.read_csv(url)

# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Div(children="DinoSource"),
    html.Hr(),
    dcc.RadioItems(options=["pop", "lifeExp", "gdpPercap"], value="lifeExp", id="my-final-radio-item-example"),
    dash_table.DataTable(data=df.to_dict("records"), page_size=6),
    dcc.Graph(figure={}, id="my-final-graph-example")
]

# Add controls to build the interaction
@callback(
    Output(component_id="my-final-graph-example", component_property="figure"),
    Input(component_id="my-final-radio-item-example", component_property="value")
)
def update_graph(col_chosen):
    fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
    return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
