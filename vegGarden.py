import pandas as pd

# pip install "pymongo[srv]"
import pymongo

# from bson.objectid import ObjectId
# from datetime import datetime
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from datetime import date  # , datetime

# datetime object containing current date and time


from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://Topaccina:1234@cluster0.uj4bmfd.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["vegGarden"]
collection = db["harvestTracking"]
print(collection)

# x = collection.find({}, {"category": "Zucchini"})

# for data in x:
#     print(data)

myFrame = pd.DataFrame(list(collection.find()))
print(myFrame)
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])


app.layout = dbc.Container(
    [
        html.H1("My vegGarden Register"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Category", html_for="Category"),
                                dcc.Dropdown(
                                    id="dd-category",
                                    options=[
                                        {"label": "Zucchini", "value": "Zucchini"},
                                        {"label": "Tomato", "value": "Tomato"},
                                    ],
                                ),
                            ],
                            className="mb-3",
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Type", html_for="Type"),
                                dcc.Dropdown(
                                    id="dd-type",
                                    options=[
                                        {
                                            "label": "Marzio-Rigato Romanesco",
                                            "value": "Marzio-Rigato Romanesco",
                                        },
                                        {"label": "Oscar", "value": "Oscar"},
                                    ],
                                ),
                            ],
                            className="mb-3",
                        )
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Date", html_for="Date "),
                                html.Br(),
                                dcc.DatePickerSingle(
                                    id="dt-picker-date",
                                    min_date_allowed=date(2000, 1, 1),
                                    max_date_allowed=date(2025, 1, 1),
                                    initial_visible_month=date(2023, 6, 1),
                                    date=date(2023, 6, 1),
                                ),
                                print(type(date(2023, 6, 1)))
                                # html.Br(),
                                # html.P(id="output"),
                            ]
                        )
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Pieces", html_for="Pieces"),
                                dbc.Input(
                                    id="in-pieces", placeholder="pieces", type="number"
                                ),
                            ]
                        )
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Weight", html_for="Weigth"),
                                dbc.Input(
                                    id="in-weight", placeholder="weight", type="number"
                                ),
                                html.Br(),
                                # html.P(id="output"),
                            ]
                        )
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                # dbc.Col([
                #     html.Div(
                #         [
                #             dbc.Textarea(className="mb-3", id='feedback',
                #                          placeholder="Write your feedback here"),
                #         ])
                # ]),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "Submit", id="submit", className="me-2", n_clicks=0
                                ),
                            ]
                        )
                    ]
                ),
            ]
        ),
        html.Hr(),
        dbc.Row([dbc.Col([html.Div([html.P("Entry Summary", id="output")])])]),
    ]
)


@app.callback(
    Output("output", "children"),
    [Input("submit", "n_clicks")],
    [
        State("dd-category", "value"),
        State("dd-type", "value"),
        State("in-weight", "value"),
        State("in-pieces", "value"),
        State("dt-picker-date", "date"),
    ],
    prevent_initial_call=True,
)
def insertNewRecord(n, opt, type, weight, n_pieces, date):
    strOut = f"Category: {opt}, Type: {type}, Weight: {weight}, n_pieces: {n_pieces}, Date: {date}"
    record = {
        "category": opt,
        "type": type,
        "weight": weight,
        "date": date,
        "pieces": n_pieces,
    }

    collection.insert_one(record)

    return strOut


if __name__ == "__main__":
    app.run_server(debug=True)
