from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent

requirements = here / 'requirements' / 'prod.txt'

readme = Path(__file__).parent / 'README.md'
with readme.open(mode='rt', encoding='utf-8') as fp:
    readme_text = fp.read()

try:
    with requirements.open(mode='rt', encoding='utf-8') as fp:
        install_requires = (line.split('#')[0].strip() for line in fp)
        install_requires = list(filter(None, install_requires))
except IndexError:
    raise RuntimeError('requirements/prod.txt is broken')

version = '0.0.2'

setup(
    name='benchmarkit',
    version=version,
    description='Benchmark and analyze functions\' time execution and results over the course of development',  # noqa
    long_description=readme_text,
    long_description_content_type='text/markdown',
    keywords=['benchmark', 'timeit', 'time'],
    license='MIT',
    author='Vitaliy Grabovets',
    author_email='v.grabovets@gmail.com',
    url='https://github.com/vgrabovets/benchmarkit',
    install_requires=install_requires,
    python_requires='>=3.6.0',
    packages=find_packages(include=['benchmarkit', 'benchmarkit.*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'benchmark_run = benchmarkit.entrypoints.run:entrypoint',
            'benchmark_analyze = benchmarkit.entrypoints.analyze:entrypoint',
        ],
    },
)
