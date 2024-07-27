import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd

# call the ability to add external scripts
external_scripts = [
    {"src": "https://cdn.tailwindcss.com"}
]

# Styles
bg_color = "black"

main_button = "relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-teal-300 to-lime-300 group-hover:from-teal-300 group-hover:to-lime-300 dark:text-white dark:hover:text-gray-900 focus:ring-4 focus:outline-none"
main_button_span = "text-xl relative px-5 py-2.5 transition-all ease-in duration-75 bg-white dark:bg-gray-900 rounded-md group-hover:bg-opacity-0 hover:font-bold"

# Initialize the app
app = dash.Dash(__name__, external_scripts=external_scripts, suppress_callback_exceptions=True)
data = pd.read_csv(
    "https://raw.githubusercontent.com/NelbaBarreto/programacion-ciencias-datos/main/data/dinosaurs_dataset.csv"
)

data["length"] = data["length"].str.replace("m", "")  # Quitar el caracter m
data["length"] = data["length"].astype(float)

data.loc[data["period"] == "USA", "period"] = "Late Cretaceous"

def substr_till_second_space(s):
    parts = s.split(" ")
    return " ".join(parts[:2])

data["full_period"] = data["period"]
data["period"] = data["full_period"].apply(substr_till_second_space)

unique_periods = list(data["period"].unique())
unique_periods.insert(0, "Todos")
periods = [{"label": period, "value": period} for period in unique_periods]

# Main layout
app.layout = html.Div(
    className="container",
    children=[
        html.H1("Análisis de Datos de Dinosaurios 🦕", className="text-5xl text-white mt-4 mb-6 text-center"),
        html.Div(
            [
                html.Button(
                    id="btn-overview",
                    n_clicks=0,
                    className=main_button,
                    children=html.Span("Overview", className=main_button_span),
                ),
                html.Button(
                    id="btn-periodo",
                    n_clicks=0,
                    className=main_button,
                    children=html.Span("Periodo", className=main_button_span),
                ),
            ],
            className="flex justify-center"
        ),
        html.Div(id="page-content", className="p-20"),
    ],
)

# Layouts for different pages
def layout_overview():
    return html.Div([
        dcc.Graph(id="grafico-dinosaurios", figure=dino_count_by_diet())
    ])

def layout_periodo():
    return html.Div([
        html.H2("Elegir un Periodo:", className="text-lime-500 font-semibold text-sm mb-2"),
        dcc.Dropdown(
            id="dropdown-period",
            options=periods,
            value="Todos",
            className="w-1/2",
        ),
        dcc.Graph(id="grafico-dinosaurios"),
    ])

# Graph for dinosaur count by diet
def dino_count_by_diet():
    fig = go.Figure(
        data=[go.Histogram(x=data["diet"], texttemplate="%{y}", textfont_size=15)],
        layout=dict(
            barcornerradius=15,
        ),
    )
    fig.update_layout(
        title="Cantidad de Dinosaurios por Tipo de Dieta",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
    )
    return fig

# Graph for dinosaur count by period
def dino_count_by_period(filtered_data):
    fig = go.Figure(
        data=[go.Histogram(x=filtered_data["period"], texttemplate="%{y}", textfont_size=15)],
        layout=dict(
            barcornerradius=15,
        ),
    )
    fig.update_layout(
        title="Cantidad de Dinosaurios por Periodo",
        xaxis_title="Periodo",
        yaxis_title="Cantidad",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
    )
    return fig

# Callback to handle button clicks and update the page content
@app.callback(
    Output("page-content", "children"),
    [Input("btn-overview", "n_clicks"), Input("btn-periodo", "n_clicks")]
)
def display_page(n_clicks_overview, n_clicks_periodo):
    ctx = dash.callback_context
    if not ctx.triggered:
        return layout_overview()
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'btn-overview':
            return layout_overview()
        elif button_id == 'btn-periodo':
            return layout_periodo()

# Callback to update the graph based on dropdown selection
@app.callback(
    Output("grafico-dinosaurios", "figure"),
    [Input("dropdown-period", "value")],
    [State("btn-periodo", "n_clicks")]
)
def update_graph(selected_period, n_clicks_periodo):
    if n_clicks_periodo is None:
        return dash.no_update

    if selected_period == "Todos":
        filtered_data = data
    else:
        filtered_data = data[data["period"] == selected_period]
    
    return dino_count_by_period(filtered_data)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
