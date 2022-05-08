import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from server import app, User

layout = html.Div([
            
            dbc.Alert(
                    [
                        html.H4("Welcome to Stablecoin Simulator!", className="alert-heading"),
                        html.P(
                            "Stablecoin simulator merupakan aplikasi yang bertujuan untuk memprediksi kestabilan dari stablecoin algoritmik. "
                            "Dengan aplikasi ini, harapannya dapat membantu stakeholder ekonomi untuk membuat kebijakan di masa depan "
                             "."
                             ),
                        html.Hr(),
                        html.P(
                            "Lengkapi parameter yang dibutuhkan, lalu klik "
                            "Prediksi " 
                            "untuk melihat hasil prediksi" 
                        ),

                    ]
                ),

            dbc.Table([html.Thead(html.Tr([html.Th("PARAMETER"), html.Th("KETERANGAN")]))] + 
            [html.Tbody([
                html.Tr([html.Td("Action"), html.Td("Jumlah transaksi dalam satu simulasi")]),
                html.Tr([html.Td("Action per day"), html.Td("Jumlah transaksi per hari")]),
                html.Tr([html.Td("Bond Range"), html.Td("Rentang batas harga untuk protokol suatu stablecoin dalam melikuidasi agunan")]),
                html.Tr([html.Td("Bond Delay"), html.Td("Waktu atau banyak transaksi hingga para pelaku pasar bereaksi terhadap perubahan yang diakibatkan oleh likuidasi agunan dan setelah itu kembali stabil")]),
                html.Tr([html.Td("Base Spread"), html.Td("Selisih antara harga jual (bid) dan nilai beli (ask) atau quotes sell dan quotes buy.")]),
                html.Tr([html.Td("Price Noise"), html.Td("Variansi atau estimasi banyaknya noise")]),
                html.Tr([html.Td("Volume & Price Moving Average Step"), html.Td("Periode perhitungan rata-rata harga dan volume")]),
                html.Tr([html.Td("Market Speed"), html.Td("Seberapa cepat traders menyadari/merespon perubahan")]),
                html.Tr([html.Td("Price Scale"), html.Td("Koefisien pengaruh keputusan para pelaku pasar terhadap harga dalam keputusan transaksi pertama kali")]),
                html.Tr([html.Td("Var Scale"), html.Td("Koefisien pengaruh keputusan para pelaku pasar terhadap fluktuasi harga terhadap keputusan transaksi selanjutnya")]),
                ])], 
            
            bordered=True)

])
# layout = html.Div([
#                 html.H1('Parameter'),
#                 dbc.Row(dbc.Col(html.Div(
#                     html.H4(dbc.Badge("PROTOCOL", color="primary", className="me-1"))
#                 ))),
#                 dbc.Row(
#                     [
#                         dbc.Col(html.Div(html.P("Bond Expiry"))),
#                         dbc.Col(html.Div(html.P("Bond Delay"))),
#                         dbc.Col(html.Div(html.P("Bond Range"))),
#                         dbc.Col(html.Div(html.P())),
#                         dbc.Col(html.Div(html.P("Trades per Day"))),
#             ]
#         ),
#                 dbc.Row(
#                     [
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="1-100",  value = 155520000, id = "bond expiry"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="",  value = 15000, id = "bond delay"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 0.9, id = "bond range min"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Max", value = 1.1, id = "bond range max"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Max", value = 15000, id = "trades per day"))),
#             ]
#         ), 
#                  dbc.Row([dbc.Col(html.Div(html.P()))
#             ]
#         ),
#                 dbc.Row(dbc.Col(html.Div(
#                     html.H4(dbc.Badge("MARKET", color="success", className="me-2"))
#                 ))),

#                 dbc.Row(
#                     [
#                         dbc.Col(html.Div(html.P("Base Spread"))),
#                         dbc.Col(html.Div(html.P("Price Noise"))),
#                         dbc.Col(html.Div(html.P("Vol MA Step"))),
#                         dbc.Col(html.Div(html.P("Price MA Step"))),
#                         dbc.Col(html.Div(html.P("Market Speed"))),
#             ]
#         ),
#                  dbc.Row(
#                     [
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100",value = 1e-3, id = "base spread"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100", value = 1e-4, id = "price noise"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100", value = 1000, id = "vol ma step"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 1000, id = "price ma step"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 0.4, id = "market speed"))),
#             ]
#         ),
#                 dbc.Row(
#                     [
#                         dbc.Col(html.Div(html.P("Price Scale"))),
#                         dbc.Col(html.Div(html.P("Var Scale"))),
#                         dbc.Col(html.Div(html.P())),
#                         dbc.Col(html.Div(html.P())),
#                         dbc.Col(html.Div(html.P())),
#             ]
#         ),
#                 dbc.Row(
#                     [
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 1e-4, id = "price scale"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 0, id = "var scale"))),
#                         dbc.Col(html.Div()),
#                         dbc.Col(html.Div()),
#                         dbc.Col(html.Div()),
#             ]
#         ),
          
#                 dbc.Row([dbc.Col(html.Div(html.P()))
#             ]
#         ),
#                 dbc.Row(dbc.Col(html.Div(
#                     html.H4(dbc.Badge("TRADER", color="danger", className="me-3"))
#                 ))),

#                 dbc.Row(
#                     [
#                         dbc.Col(html.Div(html.P("Ideal Trader"))),
#                         dbc.Col(html.Div(html.P("Average Trader"))),
#                         dbc.Col(html.Div(html.P("Basic Trader"))),
#                         dbc.Col(html.Div(html.P("Num Order Live"))),
#                         dbc.Col(html.Div(html.P("Track Freq"))),
#             ]
#         ),
#                  dbc.Row(
#                     [
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100", value = 5,id = "ideal trader"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100", value = 500,  id = "average trader"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 100,  id = "basic trader"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100",value = 300000,  id = "num order live"))),
#                         dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100", value = 15, id = "track freq"))),
                
#             ]
#         ),
        
          
#                 dbc.Row([dbc.Col(html.Div(html.H1()))
#             ]
#         ),
#                 dbc.Row([dbc.Col(html.Div(html.H1()))
#             ]
#         ),
#                 dbc.Row([dbc.Col(html.Div(
#                     dcc.Link(dbc.Button("SUBMIT", color="info", size="lg", className="me-1",id='btn-submit'),href="/page-2", refresh=False )
#                 ))
#             ]
#         ),
#         dcc.Store(id='data'), 
#         dbc.Spinner([dcc.Graph(id='grafik6'), dcc.Graph(id='grafik1'), dcc.Graph(id='grafik2'),dcc.Graph(id='grafik3'), dcc.Graph(id='grafik4'),dcc.Graph(id='grafik5')], spinner_style={"width": "5rem", "height": "5rem"}, color="primary")

#                 ] )