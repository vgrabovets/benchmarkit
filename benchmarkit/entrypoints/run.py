import argparse

from path import Path

from benchmarkit.core import benchmark_run_file


def setup_parser():
    parser = argparse.ArgumentParser(description='Run benchmarks')

    parser.add_argument(
        'path',
        type=Path,
    )

    parser.add_argument(
        '--save_dir',
        type=Path,
        default='.benchmarks_results/',
        required=False,
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
        '--comment',
        type=str,
        default='',
        required=False,
    )

    parser.add_argument(
        '--rows_limit',
        type=int,
        default=10,
        required=False,
    )

    parser.add_argument(
        '--extra_fields',
        nargs='*',
        type=str,
        default=[],
    )

    return parser


def entrypoint():
    parser = setup_parser()
    options = parser.parse_args()

    benchmark_run_file(
        options.path,
        comment=options.comment,
        save_dir=options.save_dir,
        rows_limit=options.rows_limit,
        metric=options.metric,
        bigger_is_better=options.bigger_is_better,
        extra_fields=options.extra_fields,
    )
