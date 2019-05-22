import gc
from time import sleep

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from path import Path

from benchmarkit import benchmark, benchmark_analyze, benchmark_run
from benchmarkit.core import benchmark_run_file
from tests.settings import (
    BENCHMARK_TIME_OUTPUT_FILE, DATA, NO_BENCHMARK_FUNCTIONS_FILE,
)


@benchmark(num_iters=2)
def function1():
    sleep(0.5)
    return


@benchmark(num_iters=2, save_params=True, save_output=True)
def function2(sleep_time=0.6):
    sleep(sleep_time)
    return {'sleep_time multiplication': sleep_time * 10}


@benchmark(num_iters=2, save_params=True, save_output=True)
def function3():
    sleep(0.5)
    return


def function_without_decorator():
    sleep(0.5)
    return


def test_benchmark_run():
    result = benchmark_run(
        function1,
        save_file=Path('/tmp/test_results/test_benchmark_run1.jsonl'),
        comment='test run',
    )
    assert result[0]['name'] == 'function1'
    assert round(result[0]['best_time'], -1) == 500
    assert round(result[0]['mean_time'], -1) == 500
    assert result[0]['comment'] == 'test run'

    gc.disable()
    result = benchmark_run(
        [function1, function2, function3, function_without_decorator],
        save_file='/tmp/test_results/test_benchmark_run2.jsonl',
    )
    assert len(result) == 3

    assert result[0]['name'] == 'function1'
    assert round(result[0]['best_time'], -1) == 500
    assert round(result[0]['mean_time'], -1) == 500
    assert result[0]['comment'] == ''

    assert result[1]['name'] == 'function2'
    assert round(result[1]['best_time'], -1) == 600
    assert round(result[1]['mean_time'], -1) == 600
    assert result[1]['comment'] == ''
    assert result[1]['sleep_time'] == 0.6
    assert result[1]['sleep_time multiplication'] == 6

    with pytest.raises(AssertionError):
        @benchmark(num_iters=0)
        def function4():
            sleep(0.5)
            return

    result = benchmark_run(
        function_without_decorator,
        save_file='/tmp/test_results/test_benchmark_run3.jsonl',
    )
    assert result is None

    with pytest.raises(AssertionError):
        benchmark_run(
            function1,
            save_file=Path('/tmp/test_results/test_benchmark_run1.json'),
        )


def test_benchmark_run_file():
    result = benchmark_run_file(
        DATA,
        '/tmp/test_results2',
        comment='run benchmark file',
    )
    assert result[0][0]['name'] == 'search_in_list'
    assert result[0][1]['name'] == 'search_in_set'
    assert result[0][0]['num_items'] == result[0][1]['num_items'] == 1000000
    assert result[0][0]['comment'] == result[0][1]['comment'] == 'run benchmark file'  # noqa
    assert result[0][0]['_id'] == result[0][1]['_id']

    result = benchmark_run_file(
        NO_BENCHMARK_FUNCTIONS_FILE,
        '/tmp/test_results2',
        comment='run file with no benchmark functions',
    )
    assert result == []


def test_benchmark_analyze():
    result = benchmark_analyze(DATA / 'time')
    expected = pd.Series(
        {
            'date': '2019-05-09',
            'time': '10:59:52',
            'name': 'search_in_list',
            'branch': 'master',
            'commit': 'b0f9ccc',
            'commit_date': '2019-05-07',
            'comment': 'N=100',
            'best_time': 0.0033,
            'mean_time': 0.0039,
            'mean_time_diff': np.nan,
        },
        name=0,
    )
    assert_series_equal(result.iloc[0], expected)

    expected = pd.Series(
        {
            'date': '2019-05-09',
            'time': '11:01:06',
            'name': 'total',
            'branch': 'master',
            'commit': 'b0f9ccc',
            'commit_date': '2019-05-07',
            'comment': 'N=100000',
            'best_time': 0.9576,
            'mean_time': 1.0085,
            'mean_time_diff': 0.9046,
        },
        name=3,
    )
    assert_series_equal(result.iloc[-1], expected)

    result = benchmark_analyze(
        BENCHMARK_TIME_OUTPUT_FILE,
        func_name='search_in_set',
    )
    assert len(result) == 4

    expected = pd.Series(
        {
            'date': '2019-05-09',
            'time': '11:00:47',
            'name': 'search_in_set',
            'branch': 'master',
            'commit': 'b0f9ccc',
            'commit_date': '2019-05-07',
            'comment': 'N=10000',
            'best_time': 0.0022,
            'mean_time': 0.0028,
            'mean_time_diff': 0.0002,
        },
        name=2,
    )
    assert_series_equal(result.iloc[2], expected)

    result = benchmark_analyze(BENCHMARK_TIME_OUTPUT_FILE, rows_limit=None)
    assert len(result) == 12

    result = benchmark_analyze(BENCHMARK_TIME_OUTPUT_FILE, rows_limit=1)
    assert len(result) == 3
