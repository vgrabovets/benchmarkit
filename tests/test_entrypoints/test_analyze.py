from tests.settings import (
    BENCHMARK_MODEL_OUTPUT_FILE, BENCHMARK_TIME_OUTPUT_FILE,
)


def test_entrypoint(script_runner):
    result = script_runner.run(
        'benchmark_analyze',
        BENCHMARK_TIME_OUTPUT_FILE,
    )
    assert result.success

    result = ' '.join(result.stdout.split())
    expected = (
        'File: [36mbenchmark_functions.jsonl[0m Function: '
        '[36msearch_in_list[0m date time branch commit commit_date comment '
        'best_time mean_time mean_time_diff [32m0 2019-05-09 10:59:52 master '
        'b0f9ccc 2019-05-07 N=100 0.0033 0.0039 NaN[0m 1 2019-05-09 11:00:21 '
        'master b0f9ccc 2019-05-07 N=1000 0.0126 0.0135 0.0096 2 2019-05-09 '
        '11:00:46 master b0f9ccc 2019-05-07 N=10000 0.0993 0.1011 0.0876 '
        '[31m3 2019-05-09 11:01:06 master b0f9ccc 2019-05-07 N=100000 0.9553 '
        '1.0057 0.9046[0m ----------------------------------------------------'
        '------------------------------------------------ '
        'File: [36mbenchmark_functions.jsonl[0m Function: '
        '[36msearch_in_set[0m date time branch commit commit_date comment '
        'best_time mean_time mean_time_diff [32m0 2019-05-09 10:59:53 master '
        'b0f9ccc 2019-05-07 N=100 0.0017 0.0025 NaN[0m 1 2019-05-09 11:00:22 '
        'master b0f9ccc 2019-05-07 N=1000 0.0020 0.0026 0.0001 [31m2 '
        '2019-05-09 11:00:47 master b0f9ccc 2019-05-07 N=10000 0.0022 '
        '0.0028 0.0002[0m [31m3 2019-05-09 11:01:08 master b0f9ccc '
        '2019-05-07 N=100000 0.0023 0.0028 0.0000[0m -------------------------'
        '----------------------------------------------------------------------'
        '----- File: [36mbenchmark_functions.jsonl[0m [36mTotal[0m date '
        'time branch commit commit_date comment best_time mean_time '
        'mean_time_diff [32m0 2019-05-09 10:59:52 master b0f9ccc 2019-05-07 '
        'N=100 0.0050 0.0064 NaN[0m 1 2019-05-09 11:00:21 master b0f9ccc '
        '2019-05-07 N=1000 0.0146 0.0161 0.0097 2 2019-05-09 11:00:46 master '
        'b0f9ccc 2019-05-07 N=10000 0.1015 0.1039 0.0878 [31m3 2019-05-09 '
        '11:01:06 master b0f9ccc 2019-05-07 N=100000 0.9576 1.0085 0.9046[0m '
        '----------------------------------------------------------------------'
        '------------------------------'
    )

    assert result == expected

    result = script_runner.run(
        'benchmark_analyze',
        BENCHMARK_MODEL_OUTPUT_FILE,
        '--metric=score',
        '--bigger_is_better',
        '--extra_fields=C',
    )
    assert result.success

    result = ' '.join(result.stdout.split())

    assert result == (
        'File: [36mbenchmark_model.jsonl[0m Function: '
        '[36mlog_regression[0m date time branch commit commit_date comment '
        'best_time mean_time C score score_diff [32m0 2019-05-18 12:14:14 '
        'master cd69686 2019-05-12 baseline model 67.4097 67.4097 1.0 0.973333 '
        'NaN[0m [31m1 2019-05-18 12:14:14 master cd69686 2019-05-12 stronger '
        'regularization 22.8525 22.8525 0.5 0.966667 -0.006667[0m '
        '----------------------------------------------------------------------'
        '--------------------------------------------------------'
    )
