import argparse

from path import Path

from benchmarkit.core import benchmark_run_file


def setup_parser():
    parser = argparse.ArgumentParser(description='Run benchmarks')

    parser.add_argument(
        'path',
        type=Path,
        help='Path to file or directory with files, containing benchmarks',
    )

    parser.add_argument(
        '--save_dir',
        type=Path,
        default='.benchmarks_results/',
        required=False,
        help='Path to folder where to save results',
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
        '--comment',
        type=str,
        default='',
        required=False,
        help='Comment to save alongside the results',
    )

    parser.add_argument(
        '--rows_limit',
        type=int,
        default=10,
        required=False,
        help='Limit table rows in console output. Default 10',
    )

    parser.add_argument(
        '--extra_fields',
        nargs='*',
        type=str,
        default=[],
        help='Extra fields to include in console output',
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
