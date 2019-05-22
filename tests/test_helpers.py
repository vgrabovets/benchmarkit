from colorama import Fore

from benchmarkit.helpers import color_text, get_parameters


def test_color_text():
    res = color_text('Hello, world!', Fore.GREEN)
    assert res == '[32mHello, world![0m'


def test_get_parameters():
    def test_func(param1=True, param2=111, param3=222):
        if param1:
            return param2
        return param3

    res = get_parameters(test_func)
    assert res == {'param1': True, 'param2': 111, 'param3': 222}
