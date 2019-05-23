import datetime
import gc
import json
import sys
import time
import uuid
from functools import wraps

import pandas as pd
from colorama import Fore
from git import InvalidGitRepositoryError, Repo
from path import Path

from benchmarkit.helpers import (
    DATE_FORMAT, GROUPBY_COLUMNS, TIME_FORMAT, color_text, create_table,
    df_to_string, get_parameters, process_df,
)


def benchmark(num_iters=1, save_params=False, save_output=False):
    assert num_iters > 0, 'Number of iterations should be > 0'

    try:
        repo = Repo(search_parent_directories=True)
    except InvalidGitRepositoryError:
        repo = None

    def benchmarked(func):
        @wraps(func)
        def wrapper(*args, **kw):
            times = []

            gcold = gc.isenabled()

            try:
                for _ in range(num_iters):
                    gc.enable()
                    gc.collect()
                    gc.disable()

                    t0 = time.monotonic()
                    result = func(*args, **kw)
                    t1 = time.monotonic()
                    times.append(t1 - t0)

            finally:
                if gcold:
                    gc.enable()

            best = round(min(times) * 1000, 4)
            mean = round(sum(times) / num_iters * 1000, 4)

            if repo and not repo.head.is_detached:
                branch = repo.active_branch.name
            else:
                branch = ''

            stats = {
                'name': func.__name__,
                'best_time': best,
                'mean_time': mean,
                'date': datetime.datetime.now().strftime(DATE_FORMAT),
                'time': datetime.datetime.now().strftime(TIME_FORMAT),
                'branch': branch,
                'commit': repo.head.commit.hexsha[:7] if repo else '',
                'commit_date': repo.head.commit.committed_datetime.strftime(DATE_FORMAT) if repo else '',  # noqa
            }

            if save_params:
                parameters = get_parameters(func)

                if parameters:
                    stats.update(parameters)

            if save_output and isinstance(result, dict):
                stats.update(result)

            return result, stats

        setattr(wrapper, 'run_benchmark', True)

        return wrapper

    return benchmarked


def benchmark_run(
    functions,
    save_file,
    rows_limit=10,
    comment='',
    extra_fields=None,
    metric='mean_time',
    bigger_is_better=False,
):
    save_file = Path(save_file)

    assert save_file.ext == '.jsonl', 'save_file should be path to the file with extension .jsonl'  # noqa

    save_dir = save_file.dirname()

    if not save_dir.isdir():
        save_dir.mkdir()

    if callable(functions):
        functions = [functions]

    _id = str(uuid.uuid4())

    new_entries = []

    for function in functions:
        if hasattr(function, 'run_benchmark'):
            _, stats = function()

            stats.update({
                'comment': comment[:50] if comment else '',
                '_id': _id,
            })
            new_entries.append(stats)

    with open(save_file, mode='at', encoding='utf-8') as fp:
        for new_row in new_entries:
            json.dump(new_row, fp)
            fp.write('\n')

    if new_entries:
        benchmark_analyze(
            save_file,
            func_name=None,
            rows_limit=rows_limit,
            metric=metric,
            extra_fields=extra_fields,
            bigger_is_better=bigger_is_better,
        )
    else:
        sys.stdout.write('No functions with benchmark decorator are found!\n')
        return

    return new_entries


def benchmark_run_file(
    input_path,
    save_dir='.benchmarks_results/',
    rows_limit=10,
    comment='',
    metric='mean_time',
    bigger_is_better=False,
    extra_fields=None,
):
    result = []

    input_path = Path(input_path)
    input_files = []

    if not input_path.ext:
        input_files = input_path.walkfiles(match='*.py')
    else:
        input_files.append(input_path)

    save_dir = Path(save_dir)
    if not save_dir.isdir():
        save_dir.mkdir()

    for input_file in input_files:
        input_file = Path(input_file)

        if str(input_file.name) == '__init__.py':
            continue

        save_file = save_dir / input_file.stem + '.jsonl'

        with input_file.open() as fp:
            code = compile(fp.read(), str(input_file), 'exec')
            objects = {}
            exec(code, objects)

        functions = []

        for name, obj in objects.items():
            if hasattr(obj, 'run_benchmark'):
                functions.append(obj)

        if functions:
            benchmark_results = benchmark_run(
                functions,
                save_file=save_file,
                rows_limit=rows_limit,
                comment=comment,
                metric=metric,
                bigger_is_better=bigger_is_better,
                extra_fields=extra_fields,
            )

            result.append(benchmark_results)
        else:
            sys.stdout.write(
                f'No functions with benchmark decorator in {input_file}\n',
            )

    return result


def benchmark_analyze(
    input_path,
    func_name=None,
    rows_limit=50,
    metric='mean_time',
    extra_fields=None,
    bigger_is_better=False,
):
    input_path = Path(input_path)

    input_files = []

    result = []

    if not input_path.ext:
        input_files = input_path.walkfiles(match='*.jsonl')
    else:
        input_files.append(input_path)

    for input_file in input_files:

        df = create_table(input_file)

        if func_name:
            func_names = [func_name]
        else:
            func_names = df['name'].unique()

        for name in func_names:
            temp_df = process_df(
                df[df['name'] == name],
                metric=metric,
                rows_limit=rows_limit,
                extra_fields=extra_fields,
            )

            result.append(temp_df.copy())

            temp_df.drop(columns='name', inplace=True)

            string_df = df_to_string(
                temp_df,
                metric=metric,
                bigger_is_better=bigger_is_better,
            )

            msg = (
                '\nFile: {file_name}\n'
                'Function: {func_name}\n'
                '{df}\n'
                '{separator}\n'
            ).format(
                file_name=color_text(input_file.name, Fore.CYAN) if input_file else '',  # noqa
                func_name=color_text(name, Fore.CYAN),
                df=string_df,
                separator='-' * len(string_df.split('\n')[0]),
            )

            sys.stdout.write(msg)

        # total
        if len(func_names) > 1 and metric in ['best_time', 'mean_time']:
            grouped = df.groupby(GROUPBY_COLUMNS)

            total_best = grouped['best_time'].sum().to_frame('best_time')
            total_mean = grouped['mean_time'].sum().to_frame('mean_time')
            total_date = grouped['date'].min().to_frame('date')
            total_time = grouped['time'].min().to_frame('time')

            total_df = pd.concat(
                [total_best, total_mean, total_time, total_date],
                axis=1,
                ignore_index=False,
            )
            total_df = total_df.reset_index().sort_values(
                ['date', 'time'],
                ascending=True,
            )

            total_df['name'] = 'total'

            total_df = process_df(
                total_df,
                metric=metric,
                rows_limit=rows_limit,
            )

            result.append(total_df.copy())

            total_df.drop(columns='name', inplace=True)

            total_df_string = df_to_string(
                total_df,
                metric=metric,
                bigger_is_better=False,
            )

            msg = (
                '\nFile: {file_name}\n'
                '{total}\n'
                '{df}\n'
                '{separator}\n'
            ).format(
                file_name=color_text(input_file.name, Fore.CYAN),
                total=color_text('Total', Fore.CYAN),
                df=total_df_string,
                separator='-' * len(total_df_string.split('\n')[0]),
            )

            sys.stdout.write(msg)

    return pd.concat(result, axis=0, sort=False)
