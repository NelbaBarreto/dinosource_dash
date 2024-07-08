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

# Estilos CSS para el fondo de color
styles = {
    "background": "#0f172a",
    "textColor": "#ffffff",  # Color de texto blanco
    "fontFamily": "sans-serif",
    "textAlign": "center"
}

# Diseño del la aplicación
app.layout = html.Div(style=styles, children=[
    html.H1("Dinosaur Data Analysis 🦕", style={"color": "#ffffff"}),  # Encabezado blanco

    # Botones
    html.Div([
        html.Button("Overview", id="btn-overview", n_clicks=0, style={"margin": "10px"}),
        html.Button("Periodo", id="btn-periodo", n_clicks=0, style={"margin": "10px"})
    ]),

    # Espacio para el gráfico (se actualiza dinámicamente)
    dcc.Graph(id="grafico-dinosaurios")
])

# Callback para manejar el click en los botones
@app.callback(
    Output("grafico-dinosaurios", "figure"),
    [Input("btn-overview", "n_clicks"), Input("btn-periodo", "n_clicks")]
)
def actualizar_grafico(n_clicks_overview, n_clicks_periodo):
    # Determinar cuál botón fue presionado
    boton_presionado = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    # Lógica para actualizar el gráfico según el botón presionado
    if boton_presionado == "btn-overview":
        # Lógica para el gráfico de Overview
        fig = go.Figure(data=[go.Scatter(x=data["name"], y=data.index, mode="markers")])
        fig.update_layout(title="Overview de Dinosaurios", plot_bgcolor="#0f172a", paper_bgcolor="#0f172a", font_color="#ffffff")

    elif boton_presionado == "btn-periodo":
        # Lógica para el gráfico por Período
        count_by_period = data["period"].value_counts()
        fig = go.Figure(data=[go.Bar(x=count_by_period.index, y=count_by_period)])
        fig.update_layout(title="Cantidad de Dinosaurios por Período", xaxis_title="Período", yaxis_title="Cantidad",
                          plot_bgcolor="#0f172a", paper_bgcolor="#0f172a", font_color="#ffffff")

    else:
        # Por defecto, mostrar el gráfico de Overview
        fig = go.Figure(data=[go.Scatter(x=data["name"], y=data.index, mode="markers")])
        fig.update_layout(title="Overview de Dinosaurios", plot_bgcolor="#0f172a", paper_bgcolor="#0f172a", font_color="#ffffff")

    return fig


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
