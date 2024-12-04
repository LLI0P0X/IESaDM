import asyncio

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

import orm


# app = Dash()


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
#
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
#
# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),
#
#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),
#
#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

async def main():
    app = Dash()

    listData = await orm.select_villages()
    columns = await orm.get_village_columns()
    print(listData)
    df = pd.DataFrame(listData, columns=list(columns))

    fig1 = px.line(df, x="year", y="export", color='category', width=800, height=800)
    fig1.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
    )

    fig2 = px.line(df, x="year", y="exportCapacity", color='category', width=800, height=800)
    fig2.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
    )
    app.layout = html.Div(children=[
        html.H1(children='Дашборд'),

        html.Div(children='''
            Накодил дашборд
        '''),

        dcc.Graph(
            id='export-graph',
            figure=fig1,
            # figure=fig2
        ),

        dcc.Graph(
            id='export-capacity-graph',
            # figure=fig1,
            figure=fig2
        )
    ])
    app.run(debug=True)


if __name__ == '__main__':
    asyncio.run(main())
