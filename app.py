# index page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from server import app, server
from flask_login import logout_user, current_user
from views import page1, login, login_fd, error, page2

header = html.Div(
    id='navBarrr',
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.Img(
                src='assets/icons8-tether-240.png',
                className='logo'
            ),
            html.Div(className='links', children=[
                html.Div(id='user-name', className='link'),
                html.Div(id='logout', className='link')
            ])
        ]
    )
)





CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    "background-color": "#242424"
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#1e1c15",
}

sidebar = html.Div(
    [
        
        html.Img(src='assets/icons8-tether-240.png', style={'height':'25%', 'textAlign': 'center', 'marginLeft': '20%'}),
        html.Hr(),
        html.H1(
            "Welcome!",  style={'color' : 'black',"font-weight": "bold", 'textAlign': 'center'}
        ),
        dbc.Nav(id='navBar', vertical = True, pills=True,),
    ],
    style=SIDEBAR_STYLE, #, background-image: url('images/left-half.png')
)

container1 = {
    # "display" : "flex",
    "height" : "100vh",
}

image1 = {

    "background-position": "left top",
    "background-size":  "50%" ,
    "flex": 1,
    "height": "100%",
}

GAMBAR_LAYOUT = {
    "background-color" : "#292931",
}

sidebar1 = html.Div(
    [
        html.Div(
            className='bg-image', style=image1
        ),
        dbc.Nav(id='navBar2', vertical = True, pills=True,), 
],id="navBar", className='container')
    
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)


app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    sidebar1,
    content,
], style=GAMBAR_LAYOUT)
# app.layout = html.Div(
#     [
#         html.Div([
#             html.Div(
#                 html.Div(id='page-content', className='content'),
#                 className='content-container'
#             ),
#         ], className='container-width'),
#         dcc.Location(id='url', refresh=False),
#     ]
# )


# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div([
#         navBar,
#         html.Div(id='pageContent')
#     ])
# ], id='table-wrapper')


################################################################################
# HANDLE PAGE ROUTING - IF USER NOT LOGGED IN, ALWAYS RETURN TO LOGIN SCREEN
################################################################################
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def displayPage(pathname):
    if pathname == '/':
        if current_user.is_authenticated:
            return page1.layout
        else:
            return login.layout

    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            return login.layout

    if pathname == '/page1':
        if current_user.is_authenticated:
            return page1.layout
        else:
            return login_fd.layout

    if pathname == '/page2':
        if current_user.is_authenticated:
            return page2.layout
        else:
            return login.layout

    else:
        return error.layout


################################################################################
# ONLY SHOW NAVIGATION BAR WHEN A USER IS LOGGED IN
################################################################################
@app.callback(
    Output('navBar', 'children'),
    [Input('page-content', 'children')])
def navBar(input1):
    if current_user.is_authenticated:
        navBarContents = html.Div(
    [
        html.Img(src='assets/Logo.png', style={'height':'25%', 'textAlign': 'center', 'marginLeft': '5%'}),
        dbc.Nav(
            [
                dbc.NavLink("Panduan", href="/page1", active="exact"),
                dbc.NavLink("Parameter", href="/page2", active="exact"),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),

                
            
                dbc.NavLink("Logout", href="/logout", active="exact"),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
        return navBarContents
        


    else:
        navBarContents = [
        html.Div(
            className='bg-image', style=image1
        ),
        ]

        return navBarContents



# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/':
#         return login.layout
#     elif pathname == '/login':
#         return login.layout
#     elif pathname == '/success':
#         if current_user.is_authenticated:
#             return success.layout
#         else:
#             return login_fd.layout
#     elif pathname == '/logout':
#         if current_user.is_authenticated:
#             logout_user()
#             return logout.layout
#         else:
#             return logout.layout
#     else:
#         return '404'



# @app.callback(
#     Output('user-name', 'children'),
#     [Input('page-content', 'children')])
# def cur_user(input1):
#     if current_user.is_authenticated:
#         return html.Div('Current user: ' + current_user.username)
#         # 'User authenticated' return username in get_id()
#     else:
#         return ''


@app.callback(
    Output('logout', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Logout', href='/logout', style={'color':'primary'})
    else:
        return ''


if __name__ == '__main__':
    app.run_server(debug=True)
