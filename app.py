from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
#import geopandas as gpd


#gdf_bairros = gpd.read_file('bairros.geojson')
#gdf_projecao_edificacao = gpd.read_file('projecao_edificacao.geojson')



#retornando os centroids da camada projecao_edificacao ()
#gdf_projecao_edificacao['geometry'] = gdf_projecao_edificacao[(gdf_projecao_edificacao['tp_constru'] != 'Garagem')|    (gdf_projecao_edificacao['tp_constru'] != 'Piscina')|(gdf_projecao_edificacao['tp_constru'] != 'Telheiro')|(gdf_projecao_edificacao['tp_constru'] != 'Ed�cula')].centroid

#configurando o gráfico de atividades do município
#df = gdf_projecao_edificacao.groupby('atividade_').agg('sum')
#fig = px.bar(df, x=df.index, y=df['n_paviment'], color=df['n_paviment'], barmode="group")
df = pd.read_csv("votacao_2020.csv")

bar = px.bar(df, x=df['Partido'], y=df['Votos_Validos'], 
             color=df['Partido'], height=600, hover_data=['Nome_Urna'])


options_list = ["2000 ou mais votos",
                "1500 a 1999 votos",
                "1000 a 1499 votos",
                "500 a 999 votos",
                "250 a 499 votos",
                "150 a 249 votos",
                "100 a 149 votos",
                "50 a 99 votos",
                "1 a 49 votos"]


app = Dash(__name__)

app.layout = dbc.Container(children=[
    html.H1("Estatísticas Eleições 2020", className="text-primary"),
    dbc.Row([
        dbc.Col([
            html.H3("Vereadores - Votação por Partido", className="text-primary"),
            dcc.Graph(
                figure=bar
            ),         
        ], md=8, style={'background-color': '', 'height':'600px'}),#o componente ocupara um espaço 2 col de 12

        dbc.Col([
            
        ], md=4, style={'background-color': '', 'height':'0px'})
    ]),
    html.Hr(),#quebra de linha
    html.Hr(),#quebra de linha
    dbc.Row([
        dbc.Col([
            html.H3("Votação por verador - Intervalos", className="text-primary"),
        dcc.Dropdown(
            id="my-input",
            options=options_list,
            value="2000 ou mais votos",
            clearable=False,
            style={"width":"40%"}
        ),
        html.Br(),  
        dcc.Graph(id='my-output'),         
        ], md=12, style={'background-color': '', 'height':'200px'}),#o componente ocupara um espaço 2 col de 12
    ])
], fluid=True)

#callbacks
@app.callback(
    Output('my-output', 'figure'),
    Input('my-input', 'value'))
def update_figure(option):
    if option == "2000 ou mais votos":
        filter = df[df["Votos_Validos"] >= 2000]
    elif option == "1500 a 1999 votos":
        filter = df[(df["Votos_Validos"] >= 1500) & (df["Votos_Validos"] < 2000)]
    elif option == "1000 a 1499 votos":
        filter = df[(df["Votos_Validos"] >= 1000) & (df["Votos_Validos"] < 1500)]
    elif option == "500 a 999 votos":
        filter = df[(df["Votos_Validos"] >= 500) & (df["Votos_Validos"] < 1000)]
    elif option == "250 a 499 votos":
        filter = df[(df["Votos_Validos"] >= 250) & (df["Votos_Validos"] < 500)]
    elif option == "150 a 249 votos":
        filter = df[(df["Votos_Validos"] >= 150) & (df["Votos_Validos"] < 250)]
    elif option == "100 a 149 votos":
        filter = df[(df["Votos_Validos"] >= 100) & (df["Votos_Validos"] < 150)]
    elif option == "50 a 99 votos":
        filter = df[(df["Votos_Validos"] >= 50) & (df["Votos_Validos"] < 100)]
    elif option == "1 a 49 votos":
        filter = df[(df["Votos_Validos"] >= 0) & (df["Votos_Validos"] < 50)]

    fig = px.bar(filter, x=filter['Nome'], y='Votos_Validos', height=900)


    fig.update_layout(transition_duration=500)
  
    return fig





if __name__ == '__main__':
    app.run_server(debug=True)