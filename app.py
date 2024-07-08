import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Definir el diseño del layout
app = dash.Dash(__name__)
data = pd.read_csv("https://raw.githubusercontent.com/NelbaBarreto/programacion-ciencias-datos/main/data/dinosaurs_dataset.csv")

data["length"] = data["length"].str.replace("m", "") # Quitar el caracter m
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

app.layout = html.Div(
    children=[
        html.H1("Dinosaur Data Analysis 🦕", style={"textAlign": "center"}),
        dcc.Tabs(
            children=[
                dcc.Tab(
                    label="Resumen",
                    children=[
                        dcc.Graph(
                            id="grafico-resumen",
                            style={"width": "100%", "height": 500},
                        )
                    ],
                ),
                dcc.Tab(
                    label="Período",
                    children=[
                        dcc.Dropdown(
                            id="dropdown-periodo",
                            options=unique_periods,
                            # seleccionar por defecto el primer valor de la lista
                            value=unique_periods[0],
                        ),
                        dcc.Graph(id="grafico-periodo", style={"width": "100%", "height": 500}),
                    ],
                ),
            ],
            style={"width": "100%"},
        ),
    ],
    style={
        "backgroundColor": "#0f172a",
        "color": "#ffffff",
        "fontFamily": "sans-serif",
        "padding": 20,
    },
)

# Definir el callback para el gráfico de resumen
@app.callback(
    Output("grafico-resumen", "figure"),
    Input("dropdown-periodo", "value"),
)
def actualizar_grafico_resumen(periodo_seleccionado):
    # Cargar y procesar los data de los dinosaurios
    # ... (código para cargar y procesar data)

    # Filtrar los data por período
    data_filtrados = data[data["period"] == periodo_seleccionado]

    # Crear el gráfico de resumen
    grafico_resumen = go.Figure(
        data=[
            go.Scatter(
                x=data_filtrados["name"],
                y=data_filtrados["length"],
                mode="markers",
                name="Longitud",
            )
        ],
        layout={
            "title": f"Longitud de Dinosaurios por Nombre {periodo_seleccionado}",
            "xaxis": {"title": "Nombre del Dinosaurio"},
            "yaxis": {"title": "Longitud (en metros)"},
        },
    )

    return grafico_resumen


# Definir el callback para el gráfico de período
@app.callback(
    Output("grafico-periodo", "figure"),
    Input("dropdown-periodo", "value"),
)
def actualizar_grafico_periodo(periodo_seleccionado):
    # Filtrar los datos por período
    data_filtrados = data[data["period"] == periodo_seleccionado]

    # Contar la cantidad de dinosaurios por período
    count_by_period = data_filtrados['period'].value_counts()

    # Crear el gráfico de barras
    grafico_periodo = go.Figure(
        data=[
            go.Bar(
                x=count_by_period.index,
                y=count_by_period,
                name="Cantidad de Dinosaurios"
            )
        ],
        layout={
            "title": "Cantidad de Dinosaurios por Período",
            "xaxis": {"title": "Período Geológico"},
            "yaxis": {"title": "Cantidad"},
        },
    )
    return grafico_periodo


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
