import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import random

# call the ability to add external scripts
external_scripts = [{"src": "https://cdn.tailwindcss.com"}]

# Styles
bg_color = "#111111"

MAIN_BUTTON = "relative inline-flex items-center justify-center p-1 mb-2 me-2 overflow-hidden text-gray-900 rounded-lg group bg-gradient-to-br from-teal-300 to-lime-300 group-hover:from-teal-300 group-hover:to-lime-300 focus:ring-4 focus:outline-none"
MAIN_BUTTON_SPAN = "md:text-xl text-sm relative px-5 py-2.5 transition-all ease-in duration-75 bg-white rounded-md font-semibold group-hover:bg-opacity-0 hover:font-bold"
SELECTED_MAIN_BUTTON_SPAN = "md:text-xl text-sm relative px-5 py-2.5 transition-all group bg-gradient-to-br from-teal-300 to-lime-300 rounded-md font-semibold group-hover:bg-opacity-0 hover:font-bold"
TILE = "relative inline-flex items-center justify-center p-2 mb-2 me-2 overflow-hidden text-lg font-bold text-gray-900 rounded-lg group bg-gradient-to-br from-teal-300 to-lime-300 group-hover:from-teal-300 group-hover:to-lime-300"

# Initialize the app
app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    suppress_callback_exceptions=True,
    title="dinosource",
)

server = app.server

data = pd.read_csv(
    "https://raw.githubusercontent.com/NelbaBarreto/programacion-ciencias-datos/main/data/dinosaurs_dataset.csv"
)

data["length"] = data["length"].str.replace("m", "")  # Quitar el caracter m
data["length"] = data["length"].astype(float)
# Capitalizar los valores de la columna name
data["name"] = data["name"].str.capitalize()

data.loc[data["period"] == "USA", "period"] = "Late Cretaceous"


def substr_till_second_space(s):
    parts = s.split(" ")
    return " ".join(parts[:2])


data["full_period"] = data["period"]
data["period"] = data["full_period"].apply(substr_till_second_space)

# Corregir los valores de la columna "lived_in"
data.loc[data["lived_in"] == "North Africa", "lived_in"] = "Algeria"
data.loc[data["lived_in"] == "Wales", "lived_in"] = "United Kingdom"


def get_periods_options():
    unique_periods = list(data["period"].unique())
    periods_options = [
        {
            "label": html.Span(
                period, className="ml-2 hover:text-lime-300 hover:underline"
            ),
            "value": period,
        }
        for period in unique_periods
    ]
    return periods_options


# Obtener cantidad total de dinosaurios
def get_total_count(periodo):
    if periodo == "Todos":
        return len(data)
    elif len(periodo):
        return (data["period"].isin(periodo)).sum()
    else:
        return 0


# Obtener cantidad total de países
def get_total_country_count(periodo):
    if periodo == "Todos":
        return len(data.groupby("lived_in"))
    elif len(periodo):
        res = data[data["period"].isin(periodo)].groupby("lived_in")
        return len(res)
    else:
        return 0


# Obtener cantidad total de periodos
def get_total_period_count(periodo):
    if periodo == "Todos":
        return len(data.groupby("period"))
    elif len(periodo):
        return len(periodo)
    else:
        return 0


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


def disclaimer():
    return (
        html.P(
            children=[
                html.Span("🚨 Observación: ", className="text-red-500 font-bold"),
                "Todos los datos presentados a continuación están basados en el ",
                html.A(
                    children=[html.Span("dataset")],
                    href="https://www.kaggle.com/datasets/kjanjua/jurassic-park-the-exhaustive-dinosaur-dataset",
                    target="_blank",
                    rel="noopener noreferrer",
                    className="text-lime-300 underline",
                ),
                " utilizado de fuente.",
            ],
            className="mb-2 text-white border-s-4 border-red-500",
        )
    )


# Obtener la cantidad de dinosaurios por país
def get_dino_count_by_country(periodo):
    if periodo:
        if periodo == "Todos":
            dino_count_by_country = (
                data["lived_in"].value_counts().sort_values().reset_index()
            )
        elif len(periodo):
            dino_count_by_country = (
                data[data["period"].isin(periodo)]["lived_in"]
                .value_counts()
                .sort_values()
                .reset_index()
            )

        dino_count_by_country = dino_count_by_country.merge(
            iso_df, on="lived_in", how="left"
        )
        # Escalar la columna count (para controlar el tamaño de las burbujas en el mapa)
        dino_count_by_country["scaled_count"] = MinMaxScaler().fit_transform(
            np.array(dino_count_by_country["count"]).reshape(-1, 1)
        )
        dino_count_by_country["scaled_count"] = (
            dino_count_by_country["scaled_count"] + 1
        ) * 20
        return dino_count_by_country
    else:
        dino_count_by_country = iso_df.copy()
        dino_count_by_country[["count", "scaled_count"]] = (0, 0)

        return dino_count_by_country


# Obtener top de paises por periodo
def get_countries_top_ten(periodo):
    if periodo:
        if periodo == "Todos":
            dino_count_by_country = data["lived_in"].value_counts().reset_index()
        elif len(periodo):
            dino_count_by_country = (
                data[data["period"].isin(periodo)]["lived_in"]
                .value_counts()
                .reset_index()
            )

        res_data = dino_count_by_country.nlargest(10, "count")
        return res_data.sort_values(by="count", ascending=True)
    else:
        return pd.DataFrame({"lived_in": [], "count": []})


# Main layout
app.layout = html.Div(
    className="container m-auto",
    children=[
        html.Div(
            [
                html.Div(
                    html.Span(
                        children=[
                            html.Span("dinosource ", className="hidden md:inline"),
                            "🦕",
                        ],
                        className="md:text-xl sm:text-md relative px-5 py-2.5 transition-all ease-in duration-75 bg-black text-white rounded-md font-bold font-serif",
                    ),
                    className=MAIN_BUTTON,
                ),
                html.Button(
                    id="btn-overview",
                    n_clicks=0,
                    className=MAIN_BUTTON,
                    children=html.Span(
                        "Overview", className=MAIN_BUTTON_SPAN, id="span-overview"
                    ),
                ),
                html.Button(
                    id="btn-periodo",
                    n_clicks=0,
                    className=MAIN_BUTTON,
                    children=html.Span(
                        "Periodo", className=MAIN_BUTTON_SPAN, id="span-periodo"
                    ),
                ),
                html.Button(
                    id="btn-facts",
                    n_clicks=0,
                    className=MAIN_BUTTON,
                    children=[
                        html.Span(
                            children=[
                                html.Span("Más ", className="hidden md:inline"),
                                html.Span("+", className="inline md:hidden"),
                                "Info",
                            ],
                            className=MAIN_BUTTON_SPAN,
                            id="span-facts",
                        ),
                    ],
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
            disclaimer(),
            tiles(),
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
        children=[
            disclaimer(),
            html.Div(
                [
                    dcc.Checklist(
                        id="all-or-none",
                        options=[
                            {
                                "label": html.Span(
                                    "Seleccionar/Deseleccionar Todos",
                                    className="ml-2 hover:text-lime-300 hover:underline",
                                ),
                                "value": "Todos",
                            }
                        ],
                        value=[],
                        className="mb-2",
                        labelStyle={"cursor": "pointer"},
                        inputStyle={"cursor": "pointer"},
                    ),
                    dcc.Checklist(
                        id="my-checklist",
                        options=get_periods_options(),
                        value=[],
                        className="grid sm:grid-cols-2 lg:grid-cols-3 grid-cols-1 gap-2",
                        labelStyle={"cursor": "pointer"},
                        inputStyle={"cursor": "pointer"},
                    ),
                ],
                className="text-white p-6 bg-[#111111] rounded-lg mb-2",
            ),
            html.Div(id="tiles-container", children=tiles("Todos")),
            html.Div(
                children=[
                    dcc.Graph(
                        id="grafico-periodo-paises", figure=dino_period_by_country()
                    ),
                    dcc.Graph(
                        id="grafico-top-paises", figure=dino_period_top_countries()
                    ),
                ],
                className="grid sm:grid-cols-2 grid-cols-1 w-full",
            ),
        ],
    )


# Gráficos de pantalla de facts
def layout_facts():
    data_aux = pd.DataFrame(data)

    max_length_dinosaur = data.loc[data["length"].idxmax()]
    min_length_dinosaur = data.loc[data["length"].idxmin()]
    longest_name_dinosaur = data.loc[data["name"].apply(len).idxmax()]
    shortest_name_dinosaur = data.loc[data["name"].apply(len).idxmin()]

    # Obtener el periodo más antiguo
    earliest_year = data_aux["full_period"].str.extract(r"(\d+)-\d+")
    earliest_year.fillna("0", inplace=True)
    earliest_year = earliest_year.astype(int)
    data_aux["earliest_year"] = earliest_year
    oldest_dinosaur = data.loc[data_aux["earliest_year"].idxmax()]

    # Obtener el periodo más reciente
    earliest_year = data_aux["full_period"].str.extract(r"\d+-(\d+)")
    earliest_year.fillna("999999", inplace=True)
    earliest_year = earliest_year.astype(int)
    data_aux["newest_year"] = earliest_year
    newest_dinosaur = data.loc[data_aux["newest_year"].idxmin()]

    return html.Div(
        children=[
            disclaimer(),
            html.Div(
                children=[
                    dino_card("La mayor longitud", max_length_dinosaur),
                    dino_card("La menor longitud", min_length_dinosaur),
                    dino_card("El nombre más largo", longest_name_dinosaur),
                    dino_card("El nombre más corto", shortest_name_dinosaur),
                    dino_card("El más antiguo", oldest_dinosaur),
                    dino_card("El más reciente", newest_dinosaur),
                ],
                className="grid sm:grid-cols-2 lg:grid-cols-3 grid-cols-1 gap-2",
            ),
        ],
        className="container",
    )


def tiles(periodo="Todos"):
    return html.Div(
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("icons8-dino-67.png"),
                                className="mx-auto sm:w-14 sm:h-14 w-10 h-10 mb-2",
                            ),
                            html.Span(f"{get_total_count(periodo)} dinosaurios"),
                        ],
                        className="text-center",
                    )
                ],
                className=TILE,
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("icons8-earth-100.png"),
                                className="mx-auto sm:w-14 sm:h-14 w-10 h-10 mb-2",
                            ),
                            html.Span(f"{get_total_country_count(periodo)} países"),
                        ],
                        className="text-center",
                    )
                ],
                className=TILE,
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("icons8-rock-100.png"),
                                className="mx-auto sm:w-14 sm:h-14 w-10 h-10 mb-2",
                            ),
                            html.Span(f"{get_total_period_count(periodo)} periodos"),
                        ],
                        className="text-center",
                    )
                ],
                className=TILE,
            ),
        ],
        className="grid sm:grid-cols-3 grid-cols-1 w-full",
    )


def dino_card(title, row):
    return html.Div(
        children=[
            html.H3(
                title,
                className="mb-2 text-2xl font-semibold text-white text-center",
            ),
            html.H4(
                row["name"],
                className="bg-gradient-to-r from-teal-300 to-lime-300 bg-clip-text text-transparent text-2xl font-bold",
            ),
            html.Ul(
                children=[
                    html.Li(
                        children=[
                            html.Span(
                                "Dieta: ", className="text-lime-300 font-semibold"
                            ),
                            row["diet"],
                        ]
                    ),
                    html.Li(
                        children=[
                            html.Span(
                                "Periodo: ", className="text-lime-300 font-semibold"
                            ),
                            row["full_period"],
                        ]
                    ),
                    html.Li(
                        children=[
                            html.Span(
                                "Vivió en: ", className="text-lime-300 font-semibold"
                            ),
                            row["lived_in"],
                        ]
                    ),
                    html.Li(
                        children=[
                            html.Span(
                                "Tipo: ", className="text-lime-300 font-semibold"
                            ),
                            row["type"],
                        ]
                    ),
                    html.Li(
                        children=[
                            html.Span(
                                "Longitud: ", className="text-lime-300 font-semibold"
                            ),
                            f"{row['length']} m",
                        ]
                    ),
                    html.Li(
                        children=[
                            html.Span(
                                "Taxonomía: ", className="text-lime-300 font-semibold"
                            ),
                            row["taxonomy"],
                        ]
                    ),
                    html.Li(
                        children=[
                            html.Span(
                                "Nombrado por: ",
                                className="text-lime-300 font-semibold",
                            ),
                            row["named_by"],
                        ]
                    ),
                    html.Li(
                        children=[
                            html.Span(
                                "Especie: ", className="text-lime-300 font-semibold"
                            ),
                            row["species"],
                        ]
                    ),
                ],
                className="text-white",
            ),
            html.A(
                children=[
                    html.Span("Ver Más", className="font-semibold text-dark-900")
                ],
                href=row["link"],
                target="_blank",
                rel="noopener noreferrer",
                className="inline-flex items-center p-2 rounded-lg bg-lime-300 mt-2 hover:underline",
            ),
        ],
        className="max-w-sm p-6 bg-[#111111] rounded-lg m-auto h-full",
    )


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
        xaxis_title="Longitud (m)",
        yaxis_title="Dinosaurio",
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
    )

    return fig


# Gráficos de la pantalla de Overview
def dino_overview_by_country():
    dino_count_by_country = get_dino_count_by_country("Todos")
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
        geo=dict(
            showland=True,
            showsubunits=True,
            showcountries=True,
            showocean=True,
            oceancolor="#93c5fd",
        ),
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


# Distribución Geográfica de los Dinosaurios por periodo
def dino_period_by_country(periodo="Todos"):
    dino_count_by_country = get_dino_count_by_country(periodo)

    fig1 = go.Scattergeo(
        locations=dino_count_by_country["country_iso_code"],
        mode="markers",
        marker=dict(
            size=dino_count_by_country["scaled_count"],
        ),
        text=dino_count_by_country["count"],
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
        geo=dict(
            showland=True,
            showsubunits=True,
            showcountries=True,
            showocean=True,
            oceancolor="#93c5fd",
        ),
    )

    return fig


# Top de países por periodo
def dino_period_top_countries(periodo="Todos"):
    dino_top_ten = get_countries_top_ten(periodo)

    fig1 = go.Bar(
        x=dino_top_ten["count"],
        y=dino_top_ten["lived_in"],
        texttemplate="%{x}",
        textfont_size=12,
        orientation="h",
    )

    fig = go.Figure(
        data=[fig1],
    )

    fig.update_traces(marker_color=palette)

    fig.update_layout(
        title="Top de Países por Cantidad",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
    )

    return fig


# Callback to handle button clicks and update the page content
@app.callback(
    [
        Output("page-content", "children"),
        Output("span-overview", "className"),
        Output("span-periodo", "className"),
        Output("span-facts", "className"),
    ],
    [
        Input("btn-overview", "n_clicks"),
        Input("btn-periodo", "n_clicks"),
        Input("btn-facts", "n_clicks"),
    ],
)
def display_page(n_clicks_overview, n_clicks_periodo, n_clicks_facts):
    ctx = dash.callback_context
    if not ctx.triggered:
        return (
            layout_overview(),
            SELECTED_MAIN_BUTTON_SPAN,
            MAIN_BUTTON_SPAN,
            MAIN_BUTTON_SPAN,
        )
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "btn-overview":
            return (
                layout_overview(),
                SELECTED_MAIN_BUTTON_SPAN,
                MAIN_BUTTON_SPAN,
                MAIN_BUTTON_SPAN,
            )
        elif button_id == "btn-periodo":
            return (
                layout_periodo(),
                MAIN_BUTTON_SPAN,
                SELECTED_MAIN_BUTTON_SPAN,
                MAIN_BUTTON_SPAN,
            )
        elif button_id == "btn-facts":
            return (
                layout_facts(),
                MAIN_BUTTON_SPAN,
                MAIN_BUTTON_SPAN,
                SELECTED_MAIN_BUTTON_SPAN,
            )


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


@app.callback(
    [Output("my-checklist", "value"), Output("all-or-none", "value")],
    [Input("all-or-none", "value"), Input("my-checklist", "value")],
    [State("my-checklist", "options")],
)
def update_checklists(all_selected, selected_values, options):
    ctx = dash.callback_context

    if not ctx.triggered:
        return [[option["value"] for option in options], ["Todos"]]

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "all-or-none":
        if "Todos" in all_selected:
            return [[option["value"] for option in options], ["Todos"]]
        else:
            return [[], []]

    elif triggered_id == "my-checklist":
        if len(selected_values) == len(options):
            return [selected_values, ["Todos"]]
        else:
            return [selected_values, []]


@app.callback(Output("tiles-container", "children"), [Input("my-checklist", "value")])
def update_tiles(selected_periods):
    return tiles(selected_periods)


@app.callback(
    Output("grafico-periodo-paises", "figure"), [Input("my-checklist", "value")]
)
def update_graph(selected_periods):
    return dino_period_by_country(selected_periods)


@app.callback(Output("grafico-top-paises", "figure"), [Input("my-checklist", "value")])
def update_graph(selected_periods):
    return dino_period_top_countries(selected_periods)


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
