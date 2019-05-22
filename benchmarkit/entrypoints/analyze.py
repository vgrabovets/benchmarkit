import argparse

from path import Path

from benchmarkit.core import benchmark_analyze


def setup_parser():
    parser = argparse.ArgumentParser(description='Analyze benchmarks')

    parser.add_argument(
        'path',
        type=Path,
    )

    parser.add_argument(
        '--metric',
        type=str,
        default='mean_time',
        required=False,
    )

    parser.add_argument(
        '--bigger_is_better',
        action='store_true',
    )

    parser.add_argument(
        '--extra_fields',
        nargs='*',
        type=str,
        default=[],
    )

    parser.add_argument(
        '--func_name',
        type=str,
        default='',
        required=False,
    )

    parser.add_argument(
        '--rows_limit',
        type=int,
        default=50,
        required=False,
    )

    return parser


def entrypoint():
    parser = setup_parser()
    options = parser.parse_args()

    benchmark_analyze(
        options.path,
        metric=options.metric,
        bigger_is_better=options.bigger_is_better,
        func_name=options.func_name,
        rows_limit=options.rows_limit,
        extra_fields=options.extra_fields,
    )
