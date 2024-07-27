import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# call the ability to add external scripts
external_scripts = [{"src": "https://cdn.tailwindcss.com"}]

# Styles
bg_color = "black"

main_button = "relative inline-flex items-center justify-center p-1 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-teal-300 to-lime-300 group-hover:from-teal-300 group-hover:to-lime-300 focus:ring-4 focus:outline-none"
main_button_span = "text-xl relative px-5 py-2.5 transition-all ease-in duration-75 bg-white rounded-md group-hover:bg-opacity-0 hover:font-bold"
tile = "relative inline-flex items-center justify-center py-1 px-10 mb-2 me-2 overflow-hidden text-lg font-bold text-gray-900 rounded-lg group bg-gradient-to-br from-teal-300 to-lime-300 group-hover:from-teal-300 group-hover:to-lime-300"

# Initialize the app
app = dash.Dash(
    __name__, external_scripts=external_scripts, suppress_callback_exceptions=True
)
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
# Obtener cantidad total de dinosaurios
total_count = len(data)
# Obtener cantidad total de países
total_country_count = len(data.groupby("lived_in"))
# Obtener cantidad total de periodos
total_period_count = len(data.groupby("period"))
# Obtener top 10 de dinosaurios por longitud
dino_top_ten = data.nlargest(10, "length").sort_values(by="length", ascending=False)
# Obtener cantidad de dinosaurios por país y agregar el código de país
# según ISO 3166-1 alpha-3
iso_data = {
    "South Africa": "ZAF",
    "Argentina": "ARG",
    "USA": "USA",
    "Mongolia": "MNG",
    "Egypt": "EGY",
    "Niger": "NER",
    "China": "CHN",
    "Canada": "CAN",
    "France": "FRA",
    "Uruguay": "URY",
    "Spain": "ESP",
    "Kazakhstan": "KAZ",
    "Germany": "DEU",
    "Uzbekistan": "UZB",
    "Australia": "AUS",
    "India": "IND",
    "United Kingdom": "GBR",
    "North Africa": "NAF",  # Custom code for North Africa
    "Zimbabwe": "ZWE",
    "Antarctica": "ATA",
    "Morocco": "MAR",
    "Tanzania": "TZA",
    "Japan": "JPN",
    "Brazil": "BRA",
    "Madagascar": "MDG",
    "Lesotho": "LSO",
    "Romania": "ROU",
    "Malawi": "MWI",
    "Tunisia": "TUN",
    "Russia": "RUS",
    "Wales": "GB-WLS",  # Custom code for Wales
    "Switzerland": "CHE",
}

# Convertir el diccionario a un dataframe
iso_df = pd.DataFrame.from_dict(iso_data, orient="index").reset_index()
iso_df.columns = ["lived_in", "country_iso_code"]
# Crear un dataframe de cantidad de dinosaurios por país
dino_count_by_country = data["lived_in"].value_counts().sort_values().reset_index()
# Merge
dino_count_by_country = dino_count_by_country.merge(iso_df, on="lived_in", how="left")

# Main layout
app.layout = html.Div(
    className="container",
    children=[
        html.H1(
            "Análisis de Datos de Dinosaurios 🦕",
            className="text-5xl text-white mt-4 mb-6 text-center",
        ),
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
            className="flex justify-center",
        ),
        html.Div(id="page-content", className="p-20"),
    ],
)


# Layouts for different pages
def layout_overview():
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("icons8-dino-67.png"),
                                className="mx-auto w-14 h-14 mb-2",
                            ),
                            html.Span(total_count),
                            html.Br(),
                            html.Span("Dinosaurios"),
                        ],
                        className="text-center",
                    )
                ],
                className=tile,
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("icons8-earth-100.png"),
                                className="mx-auto w-14 h-14 mb-2",
                            ),
                            html.Span(total_country_count),
                            html.Br(),
                            html.Span("Países"),
                        ],
                        className="text-center",
                    )
                ],
                className=tile,
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("icons8-rock-100.png"),
                                className="mx-auto w-14 h-14 mb-2",
                            ),
                            html.Span(total_period_count),
                            html.Br(),
                            html.Span("Periodos"),
                        ],
                        className="text-center",
                    )
                ],
                className=tile,
            ),
            dcc.Graph(id="grafico-dinosaurios", figure=dino_overview_row1()),
            dcc.Graph(id="grafico-dinosaurios-2", figure=dino_overview_row2()),
        ]
    )


def layout_periodo():
    return html.Div(
        [
            html.H2(
                "Elegir un Periodo:",
                className="text-lime-500 font-semibold text-sm mb-2",
            ),
            dcc.Dropdown(
                id="dropdown-period",
                options=periods,
                value="Todos",
                className="w-1/2",
            ),
            dcc.Graph(id="grafico-dinosaurios"),
        ]
    )


# Gráficos de la pantalla de Overview
def dino_overview_row1():
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Cantidad de Dinosaurios por Tipo de Dieta",
            "Top de Dinosaurios por Longitud (Descendente)",
        ),
    )

    fig.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
    )

    # Cantidad de Dinosaurios por Tipo de Dieta
    fig1 = go.Histogram(x=data["diet"], texttemplate="%{y}", textfont_size=15)

    # Top de Dinosaurios por Longitud
    fig2 = go.Bar(y=dino_top_ten["length"], x=dino_top_ten["name"])

    # Agregar gráficos a la figura principal
    fig.add_trace(fig1, row=1, col=1)
    fig.add_trace(fig2, row=1, col=2)
    fig.update_layout(showlegend=False)

    return fig


# Gráficos de la pantalla de Overview
def dino_overview_row2():
    # Distribución Geográfica de los Dinosaurios
    fig1 = go.Choropleth(
        locations=dino_count_by_country["country_iso_code"],
        z=dino_count_by_country["count"],
        text=dino_count_by_country["lived_in"],
        colorscale="Reds",
        autocolorscale=False,
        marker_line_color="black",
        marker_line_width=0.5,
        colorbar_title="Cantidad",
    )

    fig = go.Figure(
        data=[fig1],
    )

    fig.update_layout(
        title="Distribución Geográfica",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
        width=1200,
        height=800,
    )

    return fig


# Graph for dinosaur count by period
def dino_count_by_period(filtered_data):
    fig = go.Figure(
        data=[
            go.Histogram(
                x=filtered_data["period"], texttemplate="%{y}", textfont_size=15
            )
        ],
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
    [Input("btn-overview", "n_clicks"), Input("btn-periodo", "n_clicks")],
)
def display_page(n_clicks_overview, n_clicks_periodo):
    ctx = dash.callback_context
    if not ctx.triggered:
        return layout_overview()
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "btn-overview":
            return layout_overview()
        elif button_id == "btn-periodo":
            return layout_periodo()


# Callback to update the graph based on dropdown selection
@app.callback(
    Output("grafico-dinosaurios", "figure"),
    [Input("dropdown-period", "value")],
    [State("btn-periodo", "n_clicks")],
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
