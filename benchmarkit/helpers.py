import json
import platform
from inspect import signature

import colorama
import pandas as pd
from colorama import Fore, Style

COLUMNS = [
    'date', 'time', 'name', 'branch', 'commit', 'commit_date', 'comment',
    'best_time', 'mean_time',
]

GROUPBY_COLUMNS = ['_id', 'branch', 'commit', 'commit_date', 'comment']

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'

if platform.system() == 'Windows':
    colorama.init()


def create_table(path):
    data = []

    with open(path, mode='rt', encoding='utf-8') as fp:
        for line in fp:
            data.append(json.loads(line.strip()))

    df = pd.DataFrame.from_dict(data)

    return df


def process_df(df, metric, rows_limit, extra_fields=None):
    if not extra_fields:
        extra_fields = []

    columns = COLUMNS + extra_fields

    if metric not in columns:
        columns.append(metric)

    df = df[columns]

    df = df.dropna(axis=1, how='all')

    df[metric + '_diff'] = df[metric].diff()

    if rows_limit:
        df = df[-rows_limit:]

    df = df.reset_index().drop(columns='index')

    return df


def df_to_string(df, metric, bigger_is_better):
    string_df = df.to_string()

    if len(df) == 1:
        return string_df

    split_string_df = string_df.split('\n')

    max_rows = df.index[df[metric] == df[metric].max()]
    min_rows = df.index[df[metric] == df[metric].min()]

    if bigger_is_better is True:
        best_rows = max_rows
        worst_rows = min_rows
    else:
        best_rows = min_rows
        worst_rows = max_rows

    for row in worst_rows:
        split_string_df[row + 1] = color_text(
            split_string_df[row + 1],
            Fore.RED,
        )

    for row in best_rows:
        split_string_df[row + 1] = color_text(
            split_string_df[row + 1],
            Fore.GREEN,
        )

    return '\n'.join(split_string_df)


def color_text(text, text_color):
    return f'{text_color}{text}{Style.RESET_ALL}'


def get_parameters(func):
    result = {}

    _signature = signature(func)
    for parameter in _signature.parameters:
        result.update({parameter: _signature.parameters[parameter].default})

    return result
