import json

import requests
import pandas as pd


class FUN:
    def __init__(self, host, dataframe):
        self.host = host
        self.df = dataframe

    def get(self, url):
        result = requests.get(f'{self.host}{url}')
        return result.json()

    def post(self, url, body):
        result = requests.post(f'{self.host}{url}', json=body)
        return result.json()

    def get_cluster(self):
        dot_columns = [col for col in self.df.columns if col.find('tags') == 0 or col.find('nearby') == 0 or col.find(
            'road_conditions') == 0 or col.find('participant_categories') == 0 or col.find('weather') == 0]
        dot_columns_replaced = [col.replace('-', '') for col in self.df.columns if col.find('tags') == 0 or col.find('nearby') == 0 or col.find(
            'road_conditions') == 0 or col.find('participant_categories') == 0 or col.find('weather') == 0]
        sample_data = self.df.rename(columns={dot_columns[idx]: dot_columns_replaced[idx] for idx in range(len(dot_columns))})
        sample_data = sample_data.iloc[0].to_dict()

        for key in sample_data:
            if key not in dot_columns_replaced and key != 'point_x' and key != 'point_y':
                if key == 'dead_count' or key == 'injured_count' or key == 'participants_count':
                    sample_data[key] = int(input(f"Введите {key}:"))
                elif key == 'point_x' or key == 'point_y':
                    sample_data[key] = float(input(f"Введите {key}:"))
                else:
                    sample_data[key] = input(f"Введите {key}:")
            else:
                sample_data[key] = 0

        result = self.post('/get_cluster', sample_data)
        print(f'Серьезность ДТП: {result.dtp}')


df = pd.read_csv('./assets/dataframe.csv').drop(['Unnamed: 0'], axis=1)
funs = FUN(host='http://127.0.0.1:8000/bot', dataframe=df)

intents = [
    {
        "tag": "get_cluster",
        "patterns": [
            "Опасность региона",
            "Информация о региона",
            "ДТП по адрессу",
            "Степень опасности адресса",
        ],
        "responses": [
            "Введите данные о ДТП:"
        ],
        "operation": funs.get_cluster
    },
    {
        "tag": "help",
        "patterns": [
            "help",
            'помогите',
            'помощь',
        ],
        "responses": [
            "Если напишешь что-то кроме 'помогите' - получение серьезности ДТП"
        ]
    }
]