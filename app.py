import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# call the ability to add external scripts
external_scripts = [
    # add the tailwind cdn url hosting the files with the utility classes
    {"src": "https://cdn.tailwindcss.com"}
]

########################################
#               Estilos
########################################
bg_color = "black"

# Estilos de botón Tailwind
main_button = "relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-teal-300 to-lime-300 group-hover:from-teal-300 group-hover:to-lime-300 dark:text-white dark:hover:text-gray-900 focus:ring-4 focus:outline-none"
main_button_span = "text-xl relative px-5 py-2.5 transition-all ease-in duration-75 bg-white dark:bg-gray-900 rounded-md group-hover:bg-opacity-0 hover:font-bold"

# Definir el diseño del layout
app = dash.Dash(__name__, external_scripts=external_scripts)
data = pd.read_csv(
    "https://raw.githubusercontent.com/NelbaBarreto/programacion-ciencias-datos/main/data/dinosaurs_dataset.csv"
)

data["length"] = data["length"].str.replace("m", "")  # Quitar el caracter m
data["length"] = data["length"].astype(float)

# Corregir el valor del dato con valor periodo = USA
data.loc[data["period"] == "USA", "period"] = "Late Cretaceous"


def substr_till_second_space(s):
    parts = s.split(" ")
    return " ".join(parts[:2])


# Recortar nombre del periodo
data["full_period"] = data["period"]
data["period"] = data["full_period"].apply(substr_till_second_space)

# Listar los valores únicos de los periodos del dataset
unique_periods = list(data["period"].unique())

# Diseño del la aplicación
app.layout = html.Div(
    className="container",
    children=[
        html.H1("Dinosaur Data Analysis 🦕", className="text-5xl text-white mt-4 mb-6"),
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
            ]
        ),
        # Espacio para el gráfico (se actualiza dinámicamente)
        dcc.Graph(id="grafico-dinosaurios"),
    ],
)


# Gráfico de cantidad de dinosaurios por tipo de dieta
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


# Gráfico de cantidad de dinosaurios por periodo
def dino_count_by_period():
    fig = go.Figure(
        data=[go.Histogram(x=data["period"])],
        layout=dict(
            barcornerradius=15,
        ),
    )
    fig.update_layout(
        title="Cantidad de Dinosaurios por Período",
        xaxis_title="Período",
        yaxis_title="Cantidad",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color="#ffffff",
    )

    return fig


# Callback para manejar el click en los botones
@app.callback(
    Output("grafico-dinosaurios", "figure"),
    [Input("btn-overview", "n_clicks"), Input("btn-periodo", "n_clicks")],
)
def actualizar_grafico(n_clicks_overview, n_clicks_periodo):
    # Determinar cuál botón fue presionado
    boton_presionado = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    # Lógica para actualizar el gráfico según el botón presionado
    if boton_presionado == "btn-overview":
        fig = dino_count_by_diet()

    elif boton_presionado == "btn-periodo":
        fig = dino_count_by_period()

    else:
        fig = dino_count_by_diet()

    return fig


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
