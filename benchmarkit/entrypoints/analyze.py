import argparse

from path import Path

from benchmarkit.core import benchmark_analyze


def setup_parser():
    parser = argparse.ArgumentParser(description='Analyze benchmark results')

    parser.add_argument(
        'path',
        type=Path,
        help='Path to .jsonl file or directory with .jsonl files with benchmark results',  # noqa
    )

    parser.add_argument(
        '--metric',
        type=str,
        default='mean_time',
        required=False,
        help='Metric which is used for comparison. Default mean_time',
    )

    parser.add_argument(
        '--bigger_is_better',
        action='store_true',
        help=(
            'Whether bigger value of metric indicates that result is better. '
            'For time benchmarks should be False, for model accuracy should be '
            'True. Default False'
        ),
    )

    parser.add_argument(
        '--extra_fields',
        nargs='*',
        type=str,
        default=[],
        help='Extra fields to include in console output',
    )

    parser.add_argument(
        '--func_name',
        type=str,
        default='',
        required=False,
        help=(
            'Display statistics for particular function. If empty then all '
            'functions, stored in file, are displayed. Default empty'
        ),
    )

    parser.add_argument(
        '--rows_limit',
        type=int,
        default=10,
        required=False,
        help='Limit table rows in console output. Default 10',
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
