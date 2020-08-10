import os

import pytest


def check_aseprite():
    result = os.system('aseprite --help')
    if result == 1:
        return False
    else:
        return True


def check_aseprite_skip():
    if not check_aseprite():
        pytest.skip('Aseprite CLI is not being recognized by your system.')