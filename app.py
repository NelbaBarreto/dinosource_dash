import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random

# call the ability to add external scripts
external_scripts = [{"src": "https://cdn.tailwindcss.com"}]

# Styles
bg_color = "#111111"

main_button = "relative inline-flex items-center justify-center p-1 mb-2 me-2 overflow-hidden text-sm text-gray-900 rounded-lg group bg-gradient-to-br from-teal-300 to-lime-300 group-hover:from-teal-300 group-hover:to-lime-300 focus:ring-4 focus:outline-none"
main_button_span = "text-xl relative px-5 py-2.5 transition-all ease-in duration-75 bg-white rounded-md font-semibold group-hover:bg-opacity-0 hover:font-bold"
tile = "relative inline-flex items-center justify-center p-2 mb-2 me-2 overflow-hidden text-lg font-bold text-gray-900 rounded-lg group bg-gradient-to-br from-teal-300 to-lime-300 group-hover:from-teal-300 group-hover:to-lime-300"

# Initialize the app
app = dash.Dash(
    __name__, external_scripts=external_scripts, suppress_callback_exceptions=True
)

server = app.server

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

# Corregir los valores de la columna "lived_in"
data.loc[data["lived_in"] == "North Africa", "lived_in"] = "Algeria"
data.loc[data["lived_in"] == "Wales", "lived_in"] = "United Kingdom"

unique_periods = list(data["period"].unique())
unique_periods.insert(0, "Todos")
periods = [{"label": period, "value": period} for period in unique_periods]
# Obtener cantidad total de dinosaurios
total_count = len(data)
# Obtener cantidad total de países
total_country_count = len(data.groupby("lived_in"))
# Obtener cantidad total de periodos
total_period_count = len(data.groupby("period"))
# Definir la paleta de colores
palette = px.colors.sequential.Tealgrn + [
    "rgb(30, 105, 133)",
    "rgb(25, 85, 114)",
    "rgb(20, 70, 94)",
]
random.seed(7)
palette_random = random.sample(palette, len(palette))


# Obtener top 10 de dinosaurios por longitud
def get_dino_top_ten(ascending=False):
    if ascending:
        res_data = data.nsmallest(10, "length")
    else:
        res_data = data.nlargest(10, "length")

    return res_data.sort_values(by="length", ascending=(not ascending))


# Obtener la cantidad de dinosaurios por dieta
def get_dino_count_by_diet():
    return data.groupby("diet")["diet"].value_counts().reset_index()


# Obtener la cantidad de dinosaurios por periodo
def get_dino_count_by_period():
    return data.groupby("period")["period"].value_counts().sort_values().reset_index()


# Obtener cantidad de dinosaurios por país y agregar el código de país
# según ISO 3166-1 alpha-3
iso_data = {
    "South Africa": "ZAF",
    "Algeria": "DZA",
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
    "Switzerland": "CHE",
}

# Convertir el diccionario a un dataframe
iso_df = pd.DataFrame.from_dict(iso_data, orient="index").reset_index()
iso_df.columns = ["lived_in", "country_iso_code"]
# Crear un dataframe de cantidad de dinosaurios por país
dino_count_by_country = data["lived_in"].value_counts().sort_values().reset_index()
dino_count_by_country = dino_count_by_country.merge(iso_df, on="lived_in", how="left")

# Main layout
app.layout = html.Div(
    className="container m-auto",
    children=[
        html.Div(
            [
                html.Div(
                    html.Span(
                        f"dinosource 🦕",
                        className="text-xl relative px-5 py-2.5 transition-all ease-in duration-75 bg-black text-white rounded-md font-bold font-serif",
                    ),
                    className=main_button,
                ),
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
                html.Button(
                    id="btn-facts",
                    n_clicks=0,
                    className=main_button,
                    children=html.Span("Dino Facts", className=main_button_span),
                ),
            ],
            className="flex justify-center mt-5",
        ),
        html.Div(id="page-content", className="lg:p-10 p-2"),
    ],
)


# Layouts for different pages
def layout_overview():
    return html.Div(
        [
            html.Div(
                children=[
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(
                                        src=app.get_asset_url("icons8-dino-67.png"),
                                        className="mx-auto sm:w-14 sm:h-14 w-10 h-10 mb-2",
                                    ),
                                    html.Span(f"{total_count} dinosaurios"),
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
                                        className="mx-auto sm:w-14 sm:h-14 w-10 h-10 mb-2",
                                    ),
                                    html.Span(f"{total_country_count} países"),
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
                                        className="mx-auto sm:w-14 sm:h-14 w-10 h-10 mb-2",
                                    ),
                                    html.Span(f"{total_period_count} periodos"),
                                ],
                                className="text-center",
                            )
                        ],
                        className=tile,
                    ),
                ],
                className="grid sm:grid-cols-3 grid-cols-1",
            ),
            html.Div(
                children=[
                    dcc.Graph(id="grafico-dieta", figure=dino_overview_count_by_diet()),
                    dcc.Graph(
                        id="grafico-dieta-longitud",
                        figure=dino_overview_length_by_diet(),
                    ),
                ],
                className="grid xl:grid-cols-2 grid-cols-1 w-screen xl:w-full bg-[#111111] mb-2",
            ),
            html.Div(
                children=[
                    dcc.Loading(
                        id="loading-1",
                        children=[
                            html.Div(
                                children=[
                                    dcc.Graph(
                                        id="grafico-top-longitud",
                                        figure=dino_overview_top_by_length(),
                                    ),
                                    html.Button(
                                        id="btn-asc-desc",
                                        n_clicks=0,
                                        className="relative inline-flex items-center justify-center p-1 mb-2 me-2 bg-lime-300 overflow-hidden text-gray-900 font-semibold rounded-lg focus:ring-4 focus:outline-none hover:ring-4",
                                        children=html.Span(
                                            "Cambiar a Top Ascendente ⬆️",
                                        ),
                                    ),
                                ],
                            ),
                        ],
                        type="circle",
                    ),
                    dcc.Graph(
                        id="grafico-dieta", figure=dino_overview_count_by_period()
                    ),
                ],
                className="grid xl:grid-cols-2 grid-cols-1 w-screen xl:w-full bg-[#111111] mb-2 pb-2 pl-2",
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="grafico-distribucion",
                        figure=dino_overview_by_country(),
                        className="w-full",
                        style={"height": "50vh"},
                    ),
                ],
                className="flex flex-col items-center w-full",
            ),
        ],
    )


# Gráficos de pantalla de periodo
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
        ]
    )


# Gráficos de pantalla de facts
def layout_facts():
    return html.Div([html.Span("")])


# Gráficos de pantalla de overview


# Cantidad de dinosaurios por tipo de dieta
def dino_overview_count_by_diet():
    dino_count = get_dino_count_by_diet()

    fig = go.Figure(
        data=[
            go.Pie(
                labels=dino_count["diet"],
                values=dino_count["count"],
                hoverinfo="label+value",
                textinfo="percent",
                marker=dict(colors=palette_random),
            )
        ]
    )

    fig.update_layout(
        title="Cantidad de Dinosaurios por Tipo de Dieta",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
    )

    return fig


# Longitud de dinosaurios por tipo de dieta
def dino_overview_length_by_diet():
    unique_diets = (
        data.groupby("diet")["diet"]
        .value_counts()
        .sort_values(ascending=False)
        .reset_index()
    )
    unique_diets = unique_diets[unique_diets["count"] > 10]["diet"]

    fig = go.Figure()

    for i, diet in enumerate(unique_diets):
        fig.add_trace(
            go.Box(
                x=data[data["diet"] == diet]["diet"],
                y=data[data["diet"] == diet]["length"],
                name=diet,
                marker_color=palette_random[i % len(palette_random)],
            )
        )

    fig.update_layout(
        title="Longitud de Dinosaurios por Tipo de Dieta",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
        xaxis_title="Tipo de Dieta",
        yaxis_title="Longitud (m)",
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        showlegend=False,
    )

    return fig


# Top de Dinosaurios por Longitud
def dino_overview_top_by_length(ascending=False):
    dino_top_ten = get_dino_top_ten(ascending)

    fig1 = go.Bar(
        x=dino_top_ten["length"],
        y=dino_top_ten["name"],
        texttemplate="%{x} m",
        textfont_size=15,
        orientation="h",
    )

    fig = go.Figure(
        data=[fig1],
    )

    fig.update_traces(marker_color=palette)

    fig.update_layout(
        title="Top de Dinosaurios por Longitud",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
        xaxis_title="Dinosaurio",
        yaxis_title="Longitud (m)",
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
    )

    return fig


# Gráficos de la pantalla de Overview
def dino_overview_by_country():
    # Distribución Geográfica de los Dinosaurios
    fig1 = go.Choropleth(
        locations=dino_count_by_country["country_iso_code"],
        z=dino_count_by_country["count"],
        text=dino_count_by_country["lived_in"],
        autocolorscale=False,
        colorbar_title="Cantidad",
        colorscale=palette,
    )

    fig = go.Figure(
        data=[fig1],
    )

    fig.update_layout(
        title="Distribución Geográfica",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
        autosize=True,
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
    )

    return fig


#  Cantidad de dinosaurios por periodo
def dino_overview_count_by_period():
    dino_count = get_dino_count_by_period()

    fig1 = go.Bar(
        x=dino_count["period"],
        y=dino_count["count"],
        texttemplate="%{y}",
        textfont_size=15,
    )

    fig = go.Figure(
        data=[fig1],
    )

    fig.update_traces(marker_color=palette)

    fig.update_layout(
        title="Cantidad de Dinosaurios por Periodo",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
        xaxis_title="Periodo",
        yaxis_title="Cantidad",
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
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


@app.callback(
    Output("grafico-top-longitud", "figure"),
    Output("btn-asc-desc", "children"),
    Input("btn-asc-desc", "n_clicks"),
)
def update_top_longitud(n_clicks):
    ascending = n_clicks % 2 == 1
    figure = dino_overview_top_by_length(ascending)
    button_text = (
        "Cambiar a Top Descendente ⬇️" if ascending else "Cambiar a Top Ascendente ⬆️"
    )
    return figure, button_text


# Callback to update the graph based on dropdown selection
# @app.callback(
#     Output("grafico-dinosaurios", "figure"),
#     [Input("dropdown-period", "value")],
#     [State("btn-periodo", "n_clicks")],
# )
# def update_graph(selected_period, n_clicks_periodo):
#     if n_clicks_periodo is None:
#         return dash.no_update

#     if selected_period == "Todos":
#         filtered_data = data
#     else:
#         filtered_data = data[data["period"] == selected_period]

#     return dino_count_by_period(filtered_data)


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
