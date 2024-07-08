# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
data = pd.read_csv("https://raw.githubusercontent.com/NelbaBarreto/programacion-ciencias-datos/main/data/dinosaurs_dataset.csv")

# Initialize the app
app = Dash()

# Transformar length a un dato numérico
data["length"] = data["length"].str.replace("m", "") # Quitar el caracter m
data["length"] = data["length"].astype(float)

def substr_till_second_space(s):
    parts = s.split(" ")
    return " ".join(parts[:2])

# Recortar nombre del periodo
data["full_period"] = data["period"]
data["period"] = data["full_period"].apply(substr_till_second_space)

# Obtener el largo promedio por tipo de dieta
avg_length_by_diet = data.groupby("diet")["length"].mean().sort_values(ascending=False)

fig1 = px.bar(avg_length_by_diet, x=avg_length_by_diet.index, y=avg_length_by_diet)

# Gráfico de barras del top 5 de mayores dinosaurios
top_din_by_length = data.sort_values(by="length", ascending=False).head(5)

fig2 = px.bar(top_din_by_length, x="name", y="length")

# App layout
app.layout = [
    html.Div(children="Dino Data!"),
    html.Hr(),
    dash_table.DataTable(data=data.to_dict("records"), page_size=6),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2)
]

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
