from tests.settings import BENCHMARK_FUNCTIONS_FILE


def test_entrypoint(script_runner):
    ret = script_runner.run(
        'benchmark_run',
        BENCHMARK_FUNCTIONS_FILE,
        '--save_dir=/tmp/test_benchmarks_entrypoint',
        '--comment="test entrypoint"',
    )
    assert ret.success
    result = ' '.join(ret.stdout.split())[:153]
    expected = (
        'File: [36mbenchmark_functions.jsonl[0m Function: '
        '[36msearch_in_list[0m date time branch commit '
        'commit_date comment best_time mean_time mean_time_diff'
    )

    assert result == expected
