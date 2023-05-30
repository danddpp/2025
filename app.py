from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import json


votacao_por_bairros_df = pd.read_csv('votacao_por_bairros.csv')

#token = open(".mapbox_token").read()
bairros_geojson = json.load(open("bairros_vencedor.geojson", "r"))

bairros_geo = []
for bairro in bairros_geojson['features']:
#bairros_geojson["features"][i]["geometry"]["coordinates"])
    bairros_geo.append({
        'type': 'Feature',
        'geometry': bairro['geometry'],
        'id':bairro['properties']['nome_bairr']
    })
    #print(bairro['properties']['nome_bairr'])
bairros_geo_ok = {'type': 'FeatureCollection', 'features': bairros_geo}

bairros_csv = pd.read_csv("bairros.csv",  dtype={"nome_bairr": str})
bairros_csv.insert(2, "QT_VOTOS_1º", [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], True)
bairros_csv.insert(3, "QT_VOTOS_2º", [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], True)




bairros_geojson2 = json.load(open("bairros_geo2.geojson", "r"))

bairros_geo2 = []
for bairro in bairros_geojson2['features']:
#bairros_geojson["features"][i]["geometry"]["coordinates"])
    bairros_geo2.append({
        'type': 'Feature',
        'geometry': bairro['geometry'],
        'id':bairro['properties']['BAIRRO']
    })
    #print(bairro['properties']['nome_bairr'])
bairros_geo_ok2 = {'type': 'FeatureCollection', 'features': bairros_geo2}




df = pd.read_csv("votacao_2020.csv")

bar = px.bar(df, x=df['Partido'], y=df['Votos_Validos'], 
             color=df['Partido'], height=600, hover_data=['Nome_Urna'])


df_pie = df.groupby('Partido').agg('sum')
pie = px.pie(df, values=df['Votos_Validos'], names="Partido", hover_data=['Votos_Validos'], width=100)
options_list = ["2000 ou mais votos",
                "1500 a 1999 votos",
                "1000 a 1499 votos",
                "500 a 999 votos",
                "250 a 499 votos",
                "150 a 249 votos",
                "100 a 149 votos",
                "50 a 99 votos",
                "1 a 49 votos"]



df_secoes = pd.read_csv("votacao_2020_secoes.csv")
list_names = df_secoes.groupby("NM_VOTAVEL").agg("sum")
list_bairros = df_secoes.groupby("BAIRRO").agg("sum").index


app = Dash(__name__)
server = app.server

app.layout = dbc.Container(children=[
    html.Hr(),#quebra de linha
    dbc.Row([
           html.H1("Estatísticas Eleições Municipais - Caraguatatuba-SP 2020", className="text-primary", style={"text-align":"center"}),
           dbc.Col([
               dbc.Card([
               html.H3("Vereadores - Votação por Partido", className="text-primary"),           
               ], style={"height":"100%", "padding":"20px"})
           ], width=4),

           dbc.Col(
               dbc.Card(dcc.Graph(figure=bar, style={"height":"100%", "padding":"10px"})), width=8),
       ], style={"margin":"10px"}),


    html.Hr(),#quebra de linha
    dbc.Row([
           dbc.Col([
               dbc.Card([
                   html.H3("Votação por vereador - Intervalos", className="text-primary"),
                   html.Label("Intervalos"),
                   html.Div(
                       dcc.Dropdown(
                           id="my-input",
                           options=options_list,
                           value="150 a 249 votos",
                           clearable=False,
                           style={"width":"40%"}
                       ),
                   ),
               ], style={"height":"100%", "padding":"20px"})
           ], width=4),

           dbc.Col(
               dbc.Card(dcc.Graph(id='my-output', style={"height":"100%", "padding":"10px"})), width=8),
       ], style={"margin":"10px"}),
    
    html.Hr(),#quebra de linha
    dbc.Row([
           dbc.Col([
               dbc.Card([
                   html.H3("Distribuição de votos de um candidato por regiões e bairros", className="text-primary"),
                   html.Label("Nome"),
                   html.Div(
                       dcc.Dropdown(
                           id="my-input-regiao-bairro",
                           options=list_names.index,
                           value="ABEL GAMA",#["ABEL GAMA"],
                           clearable=False,
                           style={"width":"40%"},
                           #multi=True
                        ),
                   ),
               ], style={"height":"100%", "padding":"20px"})
           ], width=4),

           dbc.Col(
               dbc.Card(
                   html.Div(children=[
                       dcc.Graph(id="my-output-regiao", style={'display': 'inline-block', "padding":"10px"}),
                       dcc.Graph(id="my-output-bairro", style={'display': 'inline-block', "padding":"10px"})
                   ]),
               ), width=8),
       ], style={"margin":"10px"}),

    html.Hr(),#quebra de linha
    dbc.Row([
           dbc.Col([
               dbc.Card([
                   html.H3("10 + votados por cargo em um determinado bairro", className="text-primary"),
                   html.Label("Cargo"),
                   html.Div(
                       dcc.Dropdown(
                           id="my-input-cargo",
                           options=["Prefeito","Vereador"],
                           value="Prefeito",
                           clearable=False,
                           style={"width": "40%"},
                           #persistence=True,
                           #persistence_type="session",
                           #multi=True#permite selecionar mais de uma opção simultaneamente
                       ),
                   ),

                   html.Label("Bairro", style={"margin-top":"10px"}),
                   html.Div(
                       dcc.Dropdown(
                           id="my-input-bairro",
                           options=list_bairros,
                           value=list_bairros[0],
                           clearable=False,
                           style={"width": "40%"},
                           #persistence=True,
                           #persistence_type="session",
                           #multi=True#permite selecionar mais de uma opção simultaneamente
                       ),
                   ),
               ], style={"height":"100%", "padding":"20px"})
           ], width=4),

           dbc.Col(
               dbc.Card(dcc.Graph(id='my-output-cargo-bairro', style={"height":"100%", "padding":"10px"})), width=8),
       ], style={"margin":"10px"}),

       html.Hr(),#quebra de linha
       dbc.Row([
           html.H1("Candidato x Candidato", className="text-primary", style={"text-align":"center"}),
           html.Div([
                   html.Label("Candidato 1"),
                   html.Div(
                       dcc.Dropdown(
                           id="input-candidato-1",
                           options=list_names.index,
                           value="ABEL GAMA",
                           clearable=False,
                           style={"width": "40%"},
                           #persistence=True,
                           #persistence_type="session",
                           #multi=True#permite selecionar mais de uma opção simultaneamente
                       ),
                   ),

                   html.Label("Candidato 2", style={"margin-top":"10px"}),
                   html.Div(
                       dcc.Dropdown(
                           id="input-candidato-2",
                           options=list_names.index,
                           value="AGUINALDO BROW",
                           clearable=False,
                           style={"width": "40%"},
                           #persistence=True,
                           #persistence_type="session",
                           #multi=True#permite selecionar mais de uma opção simultaneamente
                       ),
                   ),
       ]),
           dbc.Col(
               dbc.Card(dcc.Graph(id="chloropleth-map", style={"height":"100%", "padding":"10px"})), width=8),
       ], style={"margin":"10px"}),


       html.Hr(),#quebra de linha
       dbc.Row([
           html.H1("Candidato", className="text-primary", style={"text-align":"center"}),
           html.Div([
                   html.Label("Candidato"),
                   html.Div(
                       dcc.Dropdown(
                           id="input-candidato",
                           options=list_names.index,
                           value="ABEL GAMA",
                           clearable=False,
                           style={"width": "40%"},
                           #persistence=True,
                           #persistence_type="session",
                           #multi=True#permite selecionar mais de uma opção simultaneamente
                       ),
                   ),
       ]),
           dbc.Col(
               dbc.Card(dcc.Graph(id="chloropleth-map2", style={"height":"100%", "padding":"10px"})), width=8),
       ], style={"margin":"10px"}),

    ])


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

    fig = px.bar(filter, x=filter['Nome'], y='Votos_Validos', height=600)
    fig.update_layout(transition_duration=500)
  
    return fig



@app.callback(
    Output('my-output-regiao', 'figure'),
    Input('my-input-regiao-bairro', 'value'))
def update_figure(option):
    
    op = df_secoes[df_secoes["NM_VOTAVEL"] == option]
    #op = df_secoes[df_secoes["NM_VOTAVEL"].isin(option)]
    candidato = op.groupby("REGIAO").agg("sum")
    
    fig = px.bar(candidato, x=candidato.index, y='QT_VOTOS', color=candidato.index, barmode="group")
    fig.update_layout(
        transition_duration=500,
        autosize=False,
        width=300,
        height=600
    )

    return fig


@app.callback(
    Output('my-output-bairro', 'figure'),
    Input('my-input-regiao-bairro', 'value'))
def update_figure(option):
    op = df_secoes[df_secoes["NM_VOTAVEL"] == option]
    #op = df_secoes[df_secoes["NM_VOTAVEL"].isin(option)]
    candidato = op.groupby("BAIRRO").agg("sum")
    
    fig = px.bar(candidato, x=candidato.index, y='QT_VOTOS', color=candidato.index)
    fig.update_layout(
        transition_duration=500,
        autosize=False,
        width=900,
        height=600,
    )
  
    return fig


@app.callback(
    Output('my-output-cargo-bairro', 'figure'),
    Input('my-input-cargo', 'value'),
    Input('my-input-bairro', 'value'))
def update_figure(cargo, bairro):
    df_bairro = df_secoes[(df_secoes["BAIRRO"] == bairro) & (df_secoes["DS_CARGO_PERGUNTA"] == cargo)]
    df_bairro_agrup = df_bairro.groupby("NM_VOTAVEL").agg("sum")
    df_output = df_bairro_agrup.sort_values('QT_VOTOS', ascending=False).head(10)

    fig = px.bar(df_output, x=df_output.index, y='QT_VOTOS', orientation="v")
    fig.update_layout(
        transition_duration=500,
        autosize=False,
        #width=1200,
        #height=900
    )
  
    return fig



@app.callback(
    Output('chloropleth-map', 'figure'),
    Input('input-candidato-1', 'value'),
    Input('input-candidato-2', 'value')
)
def update_chloroleth_map(c1, c2):
    candidato1 = df_secoes[df_secoes['NM_VOTAVEL'] == c1]
    votos_bairro_c1 = candidato1.groupby("BAIRRO").agg("sum")
    votos_bairro_c1 = votos_bairro_c1.sort_values('BAIRRO', ascending=True)

    candidato2 = df_secoes[df_secoes['NM_VOTAVEL'] == c2]
    votos_bairro_c2 = candidato2.groupby("BAIRRO").agg("sum")
    votos_bairro_c2 = votos_bairro_c2.sort_values('BAIRRO', ascending=True)

    bairros_csv.sort_values('nome_bairr', ascending=True)
     

    for b in range(len(bairros_csv)):
        qt_votos_c1 = 0
        qt_votos_c2 = 0
        for i in range(len(votos_bairro_c1)):
            #print(bairros_csv['nome_bairr'][b])
            if votos_bairro_c1.index[i] == bairros_csv['nome_bairr'][b]:
                qt_votos_c1 = votos_bairro_c1['QT_VOTOS'][i]
        for j in range(len(votos_bairro_c2)):
            if votos_bairro_c2.index[j] == bairros_csv['nome_bairr'][b]:
                qt_votos_c2 = votos_bairro_c2['QT_VOTOS'][j]
        if qt_votos_c1 > qt_votos_c2:
            bairros_csv['Vencedor'][b] = c1
            bairros_csv['QT_VOTOS_1º'][b] = qt_votos_c1
            bairros_csv['QT_VOTOS_2º'][b] = qt_votos_c2 
        if qt_votos_c2 > qt_votos_c1:
            bairros_csv['Vencedor'][b] = c2
            bairros_csv['QT_VOTOS_1º'][b] = qt_votos_c2
            bairros_csv['QT_VOTOS_2º'][b] = qt_votos_c1 
        if (qt_votos_c1 == qt_votos_c2) and (qt_votos_c1 > 0) and (qt_votos_c2 > 0):
            bairros_csv['Vencedor'][b] = 'Empate'
            bairros_csv['QT_VOTOS_1º'][b] = qt_votos_c1
            bairros_csv['QT_VOTOS_2º'][b] = qt_votos_c2
        if (qt_votos_c1 == 0) and (qt_votos_c2 == 0):
            bairros_csv['Vencedor'][b] = 'Sem votos'
            bairros_csv['QT_VOTOS_1º'][b] = 0
            bairros_csv['QT_VOTOS_2º'][b] = 0 
    
    #print(bairros_csv)


    fig = px.choropleth_mapbox(
        data_frame=bairros_csv,#dataframe com os dados 
        geojson=bairros_geo_ok,#o arquivo de feições já com a coluna id que vincula à coluna do dataframe 
        locations='nome_bairr',#atributo que vincula o dataframe ao geojson
        color=bairros_csv["Vencedor"],#a coluna do dataframe que irá colorir o mapa
        mapbox_style="open-street-map",
        center={"lat": -23.6674133,"lon":-45.4406341},
        zoom=10,
        hover_data={'nome_bairr': True, 'Vencedor': True,  'QT_VOTOS_1º': True, 'QT_VOTOS_2º': True},
        opacity=0.5,
        title="Teste"
    )

    fig.update_layout(
        margin={'r':5,'t':5,'l':5,'b':5},
    )
    return fig





@app.callback(
    Output('chloropleth-map2', 'figure'),
    Input('input-candidato', 'value'),
)
def update_chloroleth_map(c1):
    candidato1 = df_secoes[df_secoes['NM_VOTAVEL'] == c1]
    votos_bairro = candidato1.groupby("BAIRRO").agg("sum")
    votos_bairro['BAIRRO'] = votos_bairro.index 
    print(votos_bairro)
    #df_out = bairros_geo_ok.rename(columns={'BAIRRO':'nome_bairr'})
    fig = px.choropleth_mapbox(
        data_frame=votos_bairro,#dataframe com os dados 
        geojson=bairros_geo_ok2,#o arquivo de feições já com a coluna id que vincula à coluna do dataframe 
        locations='BAIRRO',#atributo que vincula o dataframe ao geojson
        color=votos_bairro["QT_VOTOS"],#a coluna do dataframe que irá colorir o mapa
        mapbox_style="open-street-map",
        center={"lat": -23.6674133,"lon":-45.4406341},
        zoom=10,
        hover_data={'BAIRRO': True, 'QT_VOTOS': True},
        opacity=0.5,
        title="Teste"
    )

    fig.update_layout(
        margin={'r':5,'t':5,'l':5,'b':5},
    )
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
