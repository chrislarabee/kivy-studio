import abc
from pathlib import Path

import jsonlines


# noinspection PyPropertyDefinition
class Node(metaclass=abc.ABCMeta):
    # noinspection PyMethodParameters
    @property
    @abc.abstractmethod
    def assoc_file(cls):
        return ''

    @abc.abstractmethod
    def process(self, data: list):
        return data


class DefaultNode(Node):
    assoc_file = ''

    def process(self, data: list):
        return data


class Handler(metaclass=abc.ABCMeta):
    def __init__(self):
        """
        Handler is designed to act as a central repository for all text-
        based game data, with as each attribute being a Node object that
        contains the processed data from a jsonl file.

        It is recommended that you create a Handler object that inherits
        from this class and which contains the attributes you'll want it
        to have on __init__ to ease code completion.
        """
        pass

    @classmethod
    def from_dir(cls, dir_path: (str, Path)):
        """
        Creates a Handler object from a directory containing jsonl
        files.

        Args:
            dir_path: The path to a directory.

        Returns: A Handler object or child object.

        """
        dir_path = Path(dir_path)
        new_handler = cls()
        for file in dir_path.iterdir():
            p = Path(file)
            if p.suffix == '.jsonl':
                data = cls._load_jsonlines(p)
                n = cls.get_node_by_assoc_file(p.stem)
                setattr(new_handler, p.stem, n)
                n().process(data)
        return new_handler

    @staticmethod
    def get_node_by_assoc_file(assoc_file: str):
        """

        Args:
            assoc_file: A string, the name of a file that corresponds to
                a Node class' assoc_file class property.

        Returns: A matching Node, or generic DefaultNode if there is no
            match.

        """
        for n in Node.__subclasses__():
            if n.assoc_file == assoc_file:
                return n
        else:
            return DefaultNode

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
