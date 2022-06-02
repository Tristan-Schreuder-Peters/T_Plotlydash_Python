from turtle import width
from dash import dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

Gemeente_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df_gem = pd.read_csv('Data_gemeentes_getransformeerd.csv', sep=";", decimal=",")
df_gem['Jaar'] = df_gem['Jaar'].astype(str)
df_gem_corr = df_gem[
    ['Gemeenteschuld', 'Overlast zwervers', 'Banen', 'Vestigingen', 'Faillisementen', '%Landbouw van vestigingen', '%Vrouw van banen', 'Aantal bijstandsuitkeringen']
    ].copy()

fig_corr = px.imshow(df_gem_corr.corr(), color_continuous_scale=['red','white', 'blue'], range_color=[-0.7, 0.7], height=500)
fig_scatter_lanbij = px.scatter(df_gem, x='%Landbouw van vestigingen', y='Aantal bijstandsuitkeringen', color='Jaar', trendline='lowess', hover_name='Gemeente', 
            labels=({"%Landbouw van vestigingen": "Landbouw vestigingen als percentage van alle vestigingen", "Aantal bijstandsuitkeringen": "Aantal bijstandsuitkeringen per 1.000 inwoners"}), 
            trendline_color_override='black', color_discrete_map={'2015': 'orange', '2016': 'purple', '2017': 'blue'}, trendline_scope='overall', height=415)
fig_box = px.box(df_gem, x="Jaar", y="Gemeenteschuld", hover_name="Gemeente", labels=({"Gemeenteschuld": "Netto gemeenteschuld per inwoner in euro's"}),
            color='Jaar', color_discrete_map={'2015': 'orange', '2016': 'purple', '2017': 'blue'}, height=500)
fig_corr.update_layout(title_text="<b>Pearson-correlatiecoëfficiëntmatrix<b>", title_x=0.5)
fig_box.update_layout(title_text="<b>Gemeenteschuld per jaar<b>", title_x=0.5)
fig_scatter_lanbij.update_layout(title_text="<b>Correlatie tussen landbouw en bijstandsuitkeringen<b>", title_x=0.5)

Gemeente_app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.Br())
    ),
    dbc.Row(
        dbc.Col(html.H1('Python Dash Gemeentes', style={'text-align': 'center', 'color': '#2a3f5f'}))
    ),
    dbc.Row(
        dbc.Col(html.Hr(), width={"size":6, "offset": 3})
    ),
    dbc.Row(
        dbc.Col(html.H6("Uitleg van de gebruikte termen", style={'color': '#2a3f5f'}), width={"size":2, "offset": 4})
    ),
    dbc.Row([
        dbc.Col(html.B(["Vestiging", html.Br(), "Gemeenteschuld", html.Br(), "Overlast zwervers", html.Br(), "Banen", html.Br(), "Vestigingen", html.Br(), "Faillisementen", 
            html.Br(), "%Landbouw van vestigingen", html.Br(), "%Vrouw van banen", html.Br(), "Aantal bijstandsuitkeringen"]), 
            style={'text-align': 'right', 'font-size': '15px', 'color': '#2a3f5f'}, width=4), 
        dbc.Col(
            html.P(["Eén bedrijfsruimte van waaruit een beroep of dienstverlenende activiteit uitgeoefend wordt.", html.Br(),  
                        "Netto gemeenteschuld per inwoner in euro's.", html.Br(), "Meldingen van overlast door zwervers per 10.000 inwoners.", html.Br(), 
                        "Aantal banen per 1.000 inwoners van 15-74 jaar.", html.Br(), "Aantal vestigingen per 1.000 inwoners van 15-74 jaar.", html.Br(), 
                        "Aantal faillisementen van bedrijven en instellingen per 1.000 vestigingen.", html.Br(), "Landbouwvestigingen als percentage van alle vestigingen.", 
                        html.Br(), "Banen die door een vrouw ingevuld worden als percentage van alle banen.", html.Br(), 
                        "Personen met bijstand of een aan bijstand gerelateerde uitkering per 1.000 inwoners."]), style={'font-size': '15px', 'color': '#2a3f5f'}, width=7),
        dbc.Col(width=1)
    ]),
    dbc.Row(
        dbc.Col(html.Hr(), width={"size":10, "offset": 1})
    ),
    dbc.Row([
        dbc.Col(dcc.Graph(id='corr_graph', figure=fig_corr)), 
        dbc.Col(dcc.Graph(id="box_plot", figure=fig_box))
        ]),
    dbc.Row(
        dbc.Col(html.Br())
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(id='scatter_lanbij_graph', figure=fig_scatter_lanbij), width={"size":10, "offset": 1})
    ),
    dbc.Row(
        dbc.Col(html.Hr())
    ),
    dbc.Row(
        dbc.Col(html.H2('Informatie per gemeente', style={'text-align': 'center', 'color': '#2a3f5f'}), width={"size":6, "offset": 3})
    ),
    dbc.Row(
        dbc.Col(html.Br())
    ),
    dbc.Row(
        dbc.Col(dcc.Dropdown(id='dropdown', options=df_gem['Gemeente'], value='Aa en Hunze', clearable=False), width={"size":6, "offset": 3})
    ), 
    dbc.Row(
        dbc.Col(html.Br())
    ),
    dbc.Row([
        dbc.Col(dcc.Graph(id='barchart_ban')), 
        dbc.Col(dcc.Graph(id='barchart_ves')), 
        dbc.Col(dcc.Graph(id='barchart_fai'))
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='barchart_bij')), 
        dbc.Col(dcc.Graph(id='barchart_sch')), 
        dbc.Col(dcc.Graph(id='barchart_ove'))
    ]),
], fluid=True)

@Gemeente_app.callback(
    Output('barchart_sch', 'figure'),
    Output('barchart_bij', 'figure'),
    Output('barchart_ove', 'figure'),
    Output('barchart_ban', 'figure'),
    Output('barchart_ves', 'figure'),
    Output('barchart_fai', 'figure'),
    Input('dropdown', 'value'))
def update_barchart(selected_Gemeente):
    filtered_df = df_gem[df_gem.Gemeente == selected_Gemeente]
    fig_bar_sch = px.bar(filtered_df, x='Jaar', y='Gemeenteschuld', hover_name='Gemeente', 
                        labels=({"Gemeenteschuld": "In euro's"}),
                        color='Jaar', color_discrete_map={'2015': 'orange', '2016': 'purple', '2017': 'blue'}, height=400)
    fig_bar_bij = px.bar(filtered_df, x='Jaar', y='Aantal bijstandsuitkeringen', hover_name='Gemeente', 
                        labels=({"Aantal bijstandsuitkeringen": "Per 1.000 inwoners"}),
                        color='Jaar', color_discrete_map={'2015': 'orange', '2016': 'purple', '2017': 'blue'}, height=400)
    fig_bar_ove = px.bar(filtered_df, x='Jaar', y='Overlast zwervers', hover_name='Gemeente', 
                        labels=({"Overlast zwervers": "Per 10.000 inwoners"}),
                        color='Jaar', color_discrete_map={'2015': 'orange', '2016': 'purple', '2017': 'blue'}, height=400)
    fig_bar_ban = px.bar(filtered_df, x='Jaar', y='Banen', hover_name='Gemeente', 
                        labels=({"Banen": "Per 1.000 inwoners van 15-74 jaar"}),
                        color='Jaar', color_discrete_map={'2015': 'orange', '2016': 'purple', '2017': 'blue'}, height=400)
    fig_bar_ves = px.bar(filtered_df, x='Jaar', y='Vestigingen', hover_name='Gemeente', 
                        labels=({"Vestigingen": "Per 1.000 inwoners van 15-74 jaar"}),
                        color='Jaar', color_discrete_map={'2015': 'orange', '2016': 'purple', '2017': 'blue'}, height=400)
    fig_bar_fai = px.bar(filtered_df, x='Jaar', y='Faillisementen', hover_name='Gemeente', 
                        labels=({"Faillisementen": "Per 1.000 vestigingen"}),
                        color='Jaar', color_discrete_map={'2015': 'orange', '2016': 'purple', '2017': 'blue'}, height=400)
    fig_bar_sch.update_layout(title_text='<b>Gemeenteschuld per inwoner<b>', title_x= 0.5)
    fig_bar_bij.update_layout(title_text='<b>Aantal bijstandsuitkeringen<b>', title_x= 0.5)
    fig_bar_ove.update_layout(title_text='<b>Meldingen overlast zwervers<b>', title_x= 0.5)
    fig_bar_ban.update_layout(title_text='<b>Aantal banen<b>', title_x= 0.5)
    fig_bar_ves.update_layout(title_text='<b>Aantal vestigingen<b>', title_x= 0.5)
    fig_bar_fai.update_layout(title_text='<b>Aantal faillisementen<b>', title_x= 0.5)
    return fig_bar_sch, fig_bar_bij, fig_bar_ove, fig_bar_ves, fig_bar_ban, fig_bar_fai

if __name__ == '__main__':
    Gemeente_app.run_server(debug=True)