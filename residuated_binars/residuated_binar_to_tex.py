"""
    A set of scripts  for automated reasoning in residuated binars
    Copyright (C) 2021  Boris Shminke

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import json
import re
from typing import Dict, List, Union

from residuated_binars.residuated_binar import (
    BOT,
    TOP,
    CayleyTable,
    ResiduatedBinar,
)


def parse_binary_operation(line: str) -> CayleyTable:
    """
    parse text describing a binary operation in Isabelle server response

    :param line: a part of Isabelle server response, representing a binary
        operation
    :returns: a Cayley table
    """
    table: CayleyTable = {}
    regex = re.compile(r"\((\d+), (\d+)\) := (\d+)")
    match = regex.search(line)
    while match is not None:
        pos = match.span()[0] + 1
        args = list(match.groups())
        if args[0] not in table:
            table[args[0]] = {}
        table[args[0]][args[1]] = args[2]
        match = regex.search(line, pos)
    return table


def parse_unary_operation(line: str) -> Dict[str, str]:
    """
    parse text describing a unary operation in Isabelle server response

    :param line: a part of Isabelle server response, representing an unary
        operation
    :returns: an inner representation of an unary operation
    """
    table: Dict[str, str] = {}
    regex = re.compile(r"(\d+) := (\d+)")
    match = regex.search(line)
    while match is not None:
        pos = match.span()[0] + 1
        args = list(match.groups())
        table[args[0]] = args[1]
        match = regex.search(line, pos)
    return table


def isabelle_format_to_binar(
    isabelle_message: str, label: str
) -> ResiduatedBinar:
    """
    :param isabelle_message: a body of reply from Isabelle server (in JSON)
    :param label: a name of the theory for which we got a relply from server
    :returns: a residuated binar
    """
    regex = re.compile(
        r"    (\w+) =\n? +\(\\<lambda>x\. _\)\n? *\(([^a-z]*)\)\n",
        re.DOTALL,
    )
    match = regex.search(isabelle_message)
    operations: Dict[str, Union[CayleyTable, Dict[str, str]]] = {}
    while match is not None:
        table: Union[CayleyTable, Dict[str, str]] = parse_binary_operation(
            match.group(2)
        )
        if not table:
            table = parse_unary_operation(match.group(2))
        operations[match.group(1)] = table
        pos = match.span()[0] + 1
        match = regex.search(isabelle_message, pos)
    return ResiduatedBinar(label, operations)


def isabelle_response_to_binar(filename: str) -> List[ResiduatedBinar]:
    """
    read file with replies from ``isabelle`` server and parse all residuated
    binars from it

    >>> import sys
    >>> if sys.version_info.major == 3 and sys.version_info.minor >= 9:
    ...     from importlib.resources import files
    ... else:
    ...     from importlib_resources import files
    >>> len(isabelle_response_to_binar(
    ...     files("residuated_binars").joinpath("resources/isabelle2.out")
    ... ))
    6

    :param filename: a name of a file to which all replies from Isabelle server
        where written
    :returns: a list of residuated binars
    """
    with open(filename, "r", encoding="utf-8") as isabelle_log:
        nodes = json.loads(
            [
                line
                for line in isabelle_log.readlines()
                if "FINISHED" in line and "lambda" in line
            ][0][9:]
        )["nodes"]
    messages = [
        (
            [
                message["message"]
                for message in node["messages"]
                if "lambda" in message["message"]
            ][:1],
            node["theory_name"].split(".")[1],
        )
        for node in nodes
    ]
    return [
        isabelle_format_to_binar(message[0][0], message[1])
        for message in messages
        if message[0] != []
    ]


def hard_coded_order(binars) -> None:
    """
    remap item names of all binars to have the same Hasse diagram

    :param binars: a list of some very specific binars
    :returns:
    """
    some_map = {
        c: c for c in [chr(ord("a") + i) for i in range(8)] + [TOP, BOT]
    }
    some_map.update({"f": "g", "g": "f"})
    binars[1].remap_symbols(some_map)
    binars[5].remap_symbols(some_map)
    some_map.update({"a": "b", "b": "a"})
    binars[2].remap_symbols(some_map)
    some_map.update({"d": "e", "e": "d"})
    binars[3].remap_symbols(some_map)
    binars[4].remap_symbols(some_map)


def generate_tex():
    """generate some TeX code"""
    models = []
    for i in [4, 7, 8, 10]:
        output_filename = f"task{i}/isabelle.out"
        models += isabelle_response_to_binar(output_filename)
    binars = [
        binar
        for binar in models
        if binar.label in {"T30", "T61", "T92", "T123", "T154", "T185"}
    ]
    for binar in binars:
        binar.canonise_symbols()
    hard_coded_order(binars)
    for binar in binars:
        print("%", binar.label)
        print(binar.latex_mult_table())
        binar.graphviz_repr().render(binar.label)


def generate_mace():
    """generate Mace4 input format"""
    models = []
    for i in [4, 7, 8, 10]:
        output_filename = f"task{i}/isabelle.out"
        models += isabelle_response_to_binar(output_filename)
    binars = [binar for binar in models if binar.label in {"T123"}]
    for binar in binars:
        print(binar.mace4_format())
        break


if __name__ == "__main__":
    generate_tex()
