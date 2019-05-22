import importlib

from path import Path


def get_folder(name):
    mod = importlib.import_module(name)
    return Path(mod.__path__[0])


DATA = get_folder('test_data')
NO_BENCHMARK_FUNCTIONS_FILE = DATA / 'time/no_benchmark_functions.py'
BENCHMARK_FUNCTIONS_FILE = DATA / 'time/benchmark_functions.py'
BENCHMARK_TIME_OUTPUT_FILE = DATA / 'time/benchmark_functions.jsonl'
BENCHMARK_MODEL_OUTPUT_FILE = DATA / 'model/benchmark_model.jsonl'
