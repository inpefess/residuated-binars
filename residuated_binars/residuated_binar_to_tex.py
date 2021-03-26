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
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

from dot2tex import dot2tex

CayleyTable = Dict[str, Dict[str, str]]


@dataclass
class ResiduatedBinar:
    """ a representation of a residuated binar (with involution) """

    label: str
    join: CayleyTable
    meet: CayleyTable
    mult: CayleyTable
    over: CayleyTable
    undr: CayleyTable
    invo: Dict[str, str]

    def less(self) -> Dict[str, List[str]]:
        """
        :returns: some representation of a 'less' relation of a lattice reduct
            of the binar
        """
        relation: Dict[str, List[str]] = dict()
        for one in self.symbols():
            relation[one] = list()
            for two in self.symbols():
                if self.join[one][two] == two and one != two:
                    relation[one].append(two)
        return relation

    def hasse(self) -> List[Tuple[str, str]]:
        """
        :returns: some representation of a Hasse diagram of a lattice reduct of
            the binar
        """
        less = {
            pair[0]: pair[1]
            for pair in sorted(
                self.less().items(),
                key=lambda key_value: len(key_value[1]),
            )
        }
        hasse = list()
        for lower in less:
            nearest = set(less[lower])
            for higher in less[lower]:
                nearest = nearest.difference(set(less[higher]))
            hasse += [(lower, neighbour) for neighbour in list(nearest)]
        return hasse

    def graphviz_repr(self) -> str:
        """
        :returns: a representation usable by ``graphviz`` of a Hasse diagram of
            a lattice reduct of the binar
        """
        graphviz_string = "graph{\n"
        graphviz_string += "\n".join(
            [f'"{pair[1]}" -- "{pair[0]}";' for pair in self.hasse()]
        )
        graphviz_string += "}"
        return graphviz_string

    def tikz_repr(self) -> str:
        """
        :returns: TeX code for ``tikz`` drawing of a Hasse diagram of a lattice
            reduct of the binar
        """
        return dot2tex(
            dot2tex(
                self.graphviz_repr(),
                texpreproc=True,
                nominsize=True,
                texmode="math",
            ),
            figonly=True,
        )

    def cardinality(self) -> int:
        """
        :returns: number of items in the binar
        """
        return len(self.mult)

    def change_symbols(self) -> None:
        """
        renumerate binar's items in a canonical way
        """
        symbol_map = {
            pair[1]: pair[0]
            for pair in zip(
                [r"\top"]
                + [chr(ord("a") + i) for i in range(self.cardinality() - 2)]
                + [r"\bot"],
                [
                    key
                    for key, value in sorted(
                        self.less().items(),
                        key=lambda key_value: len(key_value[1]),
                    )
                ],
            )
        }
        for table_name in ["mult", "join", "meet", "over", "undr"]:
            table = getattr(self, table_name)
            new_table: CayleyTable = dict()
            for one in symbol_map.keys():
                new_table[symbol_map[one]] = dict()
                for two in symbol_map.keys():
                    new_table[symbol_map[one]][symbol_map[two]] = symbol_map[
                        table[one][two]
                    ]
            setattr(self, table_name, new_table)
        new_invo: Dict[str, str] = dict()
        for one in symbol_map.keys():
            new_invo[symbol_map[one]] = symbol_map[self.invo[one]]
        self.invo = new_invo

    def symbols(self) -> List[str]:
        """
        :returns: a list of symbols denoting items of a binar
        """
        keys = list(self.mult.keys())
        pure_keys = keys.copy()
        if r"\top" in pure_keys:
            pure_keys.remove(r"\top")
        if r"\bot" in pure_keys:
            pure_keys.remove(r"\bot")
        return (
            ([r"\top"] if r"\top" in keys else [])
            + list(sorted(pure_keys))
            + ([r"\bot"] if r"\bot" in keys else [])
        )

    def latex_mult_table(self) -> str:
        """
        :returns: a LaTeX representation of a multiplication table
        """
        table = (
            "\\begin{table}[]\n"
            + "\\begin{tabular}"
            + f"{{l|{''.join((self.cardinality()) * 'l')}}}\n"
            + "$"
            + "$ & $".join([r"\cdot"] + self.symbols())
            + "$\\\\\\hline\n"
        )
        for row in self.symbols():
            table += "$" + row + "$ & "
            for col in self.symbols():
                table += "$" + self.mult[row][col] + "$"
                if col != r"\bot":
                    table += " & "
            if row != r"\bot":
                table += r"\\"
            table += "\n"
        table += "\\end{tabular}\n" + "\\end{table}\n"
        return table


def parse_binary_operation(line: str) -> CayleyTable:
    """
    parse text describing a binary operation in Isabelle server response

    :param line: a part of Isabelle server response, representing a binary
        operation
    :returns: a Cayley table
    """
    table: CayleyTable = dict()
    regex = re.compile(r"\((\d+), (\d+)\) := (\d+)")
    match = regex.search(line)
    while match is not None:
        pos = match.span()[0] + 1
        args = list(match.groups())
        if args[0] not in table:
            table[args[0]] = dict()
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
    table: Dict[str, str] = dict()
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
    args: Dict[str, Union[str, CayleyTable, Dict[str, str]]] = {"label": label}
    while match is not None:
        table: Union[CayleyTable, Dict[str, str]] = parse_binary_operation(
            match.group(2)
        )
        if table == dict():
            table = parse_unary_operation(match.group(2))
        args[match.group(1)] = table
        pos = match.span()[0] + 1
        match = regex.search(isabelle_message, pos)
    return ResiduatedBinar(**args)  # type: ignore


def isabelle_response_to_binar(filename: str) -> List[ResiduatedBinar]:
    """
    read file with replies from ``isabelle`` server and parse all residuated
    binars from it

    :param filename: a name of a file to which all replies from Isabelle server
        where written
    :returns: a list of residuated binars
    """
    with open(filename, "r") as isabelle_log:
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


def parse_args(args: Optional[List[str]] = None) -> Namespace:
    """

    :param args: a list of string arguments
        (for testing and use in a non script scenario)
    :returns: arguments namespace for the script
    """
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--filename", type=str, required=True)
    parsed_args = argument_parser.parse_args(args)
    return parsed_args


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
    binar.change_symbols()
    print("%", binar.label)
    print(binar.latex_mult_table())
    print(binar.tikz_repr())
