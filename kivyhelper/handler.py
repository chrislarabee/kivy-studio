from pathlib import Path

import jsonlines


class Handler:
    def __init__(self):
        pass

    @staticmethod
    def _load_jsonlines(file_path: (str, Path)) -> list:
        """
        Loads a jsonlines file into a list of dictionaries.

        Args:
            file_path: The path to a .jsonl or .jsonlines file.

        Returns: A list of dictionaries, one for each line in the file.

        """
        results = []
        with jsonlines.open(file_path) as r:
            for line in r:
                results.append(line)
        return results
