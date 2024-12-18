import asyncio

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

import orm


async def main():
    listData = await orm.select_villages()
    columns = await orm.get_village_columns()
    print(listData)
    df = pd.DataFrame(listData, columns=list(columns))

    figs = []

    fig = px.line(df, x="year", y="export", color='category', title="Экспорт", width=800, height=400)
    figs.append(fig)

    fig = px.line(df, x="year", y="exportCapacity", color='category', title="Экспортный потенциал", width=800,
                  height=400)
    figs.append(fig)

    fig = px.line(df, x="year", y="importsmth", color='category', title="Импорт", width=800,
                  height=400)
    figs.append(fig)

    for _fig in figs:
        _fig.update_layout(
            margin=dict(l=20, r=20, t=70, b=20),
            paper_bgcolor="LightSteelBlue",
            plot_bgcolor="white",
            font=dict(family="Arial, sans-serif", size=14, color="black"),
            legend=dict(title="Category", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

    # Пример данных для структуры экспорта АПК в 2021 году
    export_structure_2021 = {
        'Категория продукции': ['Рыба', 'Молоко', 'Мясо', 'Кондитерские изделия',
                                'Картофель', "Подсолнечное масло", "Зерно", "Сахар"],
        'Доля в экспорте (%)': [13, 2, 2, 7, 7, 19, 37, 12]
    }

    # Пример данных для динамики экспорта АПК
    export_dynamics = {
        'Год': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        'Экспорт (млрд долл. США)': [25.8, 25.5, 30.2, 36.8, 42, 43.5, 44.6]
    }

    # Пример данных для анализа экспорта пшеницы
    data_wheat = {
        'Страна': ['Китай', 'Египет', 'Турция', 'Иран', 'Пакистан', 'Судан', 'Бангладеш', 'Нигерия', 'Вьетнам',
                   'Индонезия'],
        'Емкость рынка (тонн)': [10000000, 5000000, 4000000, 3000000, 2500000, 2000000, 1500000, 1000000, 500000,
                                 250000],
        'Емкость рынка (млн USD)': [3000, 1500, 1200, 900, 750, 600, 450, 300, 150, 75],
        'Импорт (тонн)': [5000000, 3000000, 2000000, 1500000, 1250000, 1000000, 750000, 500000, 250000, 125000],
        'Импорт (млн USD)': [1500, 900, 600, 450, 375, 300, 225, 150, 75, 37.5],
        'Доля российского экспорта (%)': [30, 60, 50, 40, 50, 50, 50, 50, 50, 50]
    }

    # Пример данных для анализа экспорта российского продовольствия
    data_food = {
        'Страна': ['Китай', 'Казахстан', 'Беларусь', 'Турция', 'Египет'],
        'Экспортный потенциал': [1000, 800, 700, 600, 500],
        'Реальный экспорт': [900, 750, 650, 550, 450],
        'Емкость рынка': [5000, 4000, 3500, 3000, 2500],
        'Доля российского экспорта': [0.18, 0.19, 0.185, 0.183, 0.18]
    }

    # Преобразование данных в DataFrame
    df_structure = pd.DataFrame(export_structure_2021)
    df_dynamics = pd.DataFrame(export_dynamics)
    df_wheat = pd.DataFrame(data_wheat)
    df_food = pd.DataFrame(data_food)

    # Создание пирожковой диаграммы для структуры экспорта
    fig_pie = px.pie(df_structure, values='Доля в экспорте (%)', names='Категория продукции',
                     title='Структура российского экспорта продукции АПК в 2021 году')

    # Создание графика для динамики экспорта
    fig_line = px.line(df_dynamics, x='Год', y='Экспорт (млрд долл. США)',
                       title='Динамика экспорта продукции АПК (2018-2024 гг.)')

    # Добавление целевого значения на график
    fig_line.add_hline(y=45, line_dash="dash", line_color="red", annotation_text="Целевое значение: 45 млрд долл. США")

    app = Dash(__name__)

    app.layout = html.Div(style={'backgroundColor': 'LightSteelBlue', 'padding': '20px'}, children=[
        html.H1("Анализ экспорта и импорта",
                style={'textAlign': 'center', 'color': 'white', 'fontFamily': 'Arial'}),
        html.P("Учебный дашборд.",
               style={'textAlign': 'center', 'color': 'white', 'fontFamily': 'Arial'}),

        html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px 0'}, children=[
            dcc.Graph(id='export-graph', figure=figs[0]),
            dcc.Graph(id='export-capacity-graph', figure=figs[1]),
        ]),
        html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px 0'}, children=[
            dcc.Graph(id='import-graph', figure=figs[2])
        ]),

        html.H1("Дашборд экспорта продукции АПК России"),

        html.Div([
            dcc.Graph(figure=fig_pie),
            dcc.Graph(figure=fig_line)
        ]),

        html.H2("Анализ экспорта пшеницы"),

        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Емкость рынка (тонн)', 'value': 'Емкость рынка (тонн)'},
                {'label': 'Емкость рынка (млн USD)', 'value': 'Емкость рынка (млн USD)'},
                {'label': 'Импорт (тонн)', 'value': 'Импорт (тонн)'},
                {'label': 'Импорт (млн USD)', 'value': 'Импорт (млн USD)'}
            ],
            value='Емкость рынка (тонн)'
        ),

        dcc.Graph(id='bar-chart'),

        dcc.Graph(id='pie-chart'),

        html.H2("Анализ экспорта российского продовольствия"),

        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df_food['Страна']],
            value='Китай'
        ),
        dcc.Graph(id='bar-chart-food'),

        dcc.Graph(id='line-chart-food')
    ])

    @app.callback(
        Output('bar-chart', 'figure'),
        [Input('metric-dropdown', 'value')]
    )
    def update_bar_chart(selected_metric):
        fig = px.bar(df_wheat, x='Страна', y=selected_metric, title=f'Рэнкинг стран по {selected_metric}')
        return fig

    @app.callback(
        Output('pie-chart', 'figure'),
        [Input('metric-dropdown', 'value')]
    )
    def update_pie_chart(selected_metric):
        fig = px.pie(df_wheat, names='Страна', values=selected_metric, title=f'Доля стран по {selected_metric}')
        return fig

    @app.callback(
        Output('bar-chart-food', 'figure'),
        [Input('country-dropdown', 'value')]
    )
    def update_bar_chart_food(selected_country):
        filtered_df = df_food[df_food['Страна'] == selected_country]
        fig = px.bar(filtered_df, x='Страна', y=['Экспортный потенциал', 'Реальный экспорт'], barmode='group')
        return fig

    @app.callback(
        Output('line-chart-food', 'figure'),
        [Input('country-dropdown', 'value')]
    )
    def update_line_chart_food(selected_country):
        filtered_df = df_food[df_food['Страна'] == selected_country]
        print(selected_country)

        n = filtered_df['Доля российского экспорта'].values[0]
        data = [n, 1 - n]
        labels = ["Доля российского экспорта", "Остальные"]
        fig = px.pie(values=data, names=labels)

        # fig = px.pie(names='Страна', values=[85, 15])
        return fig

    app.run_server(debug=True)


if __name__ == '__main__':
    asyncio.run(main())
