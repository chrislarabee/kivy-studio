import json


def enquote(x) -> str:
    """
    Wraps an object in double quotes. Convenience function to resolve
    deeply nested single and double quote conflicts in python strings.

    Args:
        x: Any object

    Returns: A string, the object as a string wrapped in double quotes.

    """
    return '"' + str(x) + '"'


def print_pycharm_bar():
    print('=' * 96)


def read_aseprite_json(file_path: str) -> dict:
    """
    Aseprite produces json files with a lot of line breaks, which is
    nice for human readability but requires a slightly specialized read
    function.

    Args:
        file_path: The path to the json file to read.

    Returns: A dictionary containing the aseprite json file's data.

    """
    json_str = ''
    with open(file_path, 'r') as r:
        for line in r:
            json_str += line.strip()
    return json.loads(json_str)
