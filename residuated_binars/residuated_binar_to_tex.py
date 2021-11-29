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
from typing import Any, Dict, List, Tuple, Union

import graphviz

CayleyTable = Dict[str, Dict[str, str]]
TOP = r"⟙"
BOT = r"⟘"


class ResiduatedBinar:
    r"""
        a representation of a residuated binar (with involution)

    >>> binar = ResiduatedBinar(
    ...     label="test",
    ...     operations={
    ...         "join": {"0": {"0": "0", "1": "1"}, "1": {"0": "1", "1": "1"}},
    ...         "meet": {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "1"}},
    ...         "mult": {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "0"}},
    ...         "over": {"0": {"0": "1", "1": "1"}, "1": {"0": "1", "1": "1"}},
    ...         "undr": {"0": {"0": "1", "1": "1"}, "1": {"0": "1", "1": "1"}},
    ...         "invo": {"0": "1", "1": "0"}
    ...     }
    ... )
    >>> binar.canonise_symbols()
    >>> binar.less()
    {'⟙': [], '⟘': ['⟙']}
    >>> binar.hasse()
    [('⟘', '⟙')]
    >>> print(binar.graphviz_repr())
    graph {
        "⟘" -- "⟙"
    }
    >>> print(binar.mace4_format())
    0 ^ 0 = 0.
    0 v 0 = 0.
    0 \ 0 = 0.
    0 / 0 = 0.
    0 * 0 = 1.
    0 ^ 1 = 1.
    0 v 1 = 0.
    0 \ 1 = 0.
    0 / 1 = 0.
    0 * 1 = 1.
    1 ^ 0 = 1.
    1 v 0 = 0.
    1 \ 0 = 0.
    1 / 0 = 0.
    1 * 0 = 1.
    1 ^ 1 = 1.
    1 v 1 = 1.
    1 \ 1 = 0.
    1 / 1 = 0.
    1 * 1 = 1.
    <BLANKLINE>
    >>> print(binar.latex_mult_table())
    \begin{table}[]
    \begin{tabular}{l|ll}
    $\cdot$ & $0$ & $1$\\\hline
    $0$ & $1$ & $1$ & \\
    $1$ & $1$ & $1$ & \\
    \end{tabular}
    \end{table}
    <BLANKLINE>
    >>> print("this_is_a_test_case", binar.tabular_format())
    this_is_a_test_case {'^': [[0, 1], [1, 1]], 'v': [[0, 0], [0, 1]], '*': [[1, 1], [1, 1]], '\\': [[0, 0], [0, 0]], '/': [[0, 0], [0, 0]]}
    """

    def __init__(
        self,
        label: str,
        operations: Dict[str, Dict[str, Any]],
    ):
        self.label = label
        self.join: CayleyTable = operations["join"]
        self.meet: CayleyTable = operations["meet"]
        self.mult: CayleyTable = operations["mult"]
        self.over: CayleyTable = operations["over"]
        self.undr: CayleyTable = operations["undr"]
        self.invo: Dict[str, str] = (
            operations["invo"] if operations["invo"] is not None else {}
        )

    def less(self) -> Dict[str, List[str]]:
        """
        :returns: some representation of a 'less' relation of a lattice reduct
            of the binar
        """
        relation: Dict[str, List[str]] = {}
        for one in self.symbols:
            relation[one] = []
            for two in self.symbols:
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
        hasse = []
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
        graph = graphviz.Graph()
        for pair in self.hasse():
            graph.edge(pair[0], pair[1])
        return graph

    def cardinality(self) -> int:
        """
        :returns: number of items in the binar
        """
        return len(self.mult)

    def canonise_symbols(self) -> None:
        """
        renumerate binar's items in a canonical way
        """
        symbol_map = {
            pair[1]: pair[0]
            for pair in zip(
                [TOP]
                + [chr(ord("a") + i) for i in range(self.cardinality() - 2)]
                + [BOT],
                [
                    key
                    for key, value in sorted(
                        self.less().items(),
                        key=lambda key_value: (
                            len(key_value[1]),
                            key_value[0],
                        ),
                    )
                ],
            )
        }
        self.remap_symbols(symbol_map)

    def remap_symbols(self, symbol_map: Dict[str, str]) -> None:
        """rename symbols in a given way"""
        for table_name in ["mult", "join", "meet", "over", "undr"]:
            table = getattr(self, table_name)
            new_table: CayleyTable = {}
            for one in symbol_map.keys():
                new_table[symbol_map[one]] = {}
                for two in symbol_map.keys():
                    new_table[symbol_map[one]][symbol_map[two]] = symbol_map[
                        table[one][two]
                    ]
            setattr(self, table_name, new_table)
        new_invo: Dict[str, str] = {}
        for one in symbol_map.keys():
            new_invo[symbol_map[one]] = symbol_map[self.invo[one]]
        self.invo = new_invo

    @property
    def symbols(self) -> List[str]:
        """
        :returns: a list of symbols denoting items of a binar
        """
        keys = list(self.mult.keys())
        pure_keys = keys.copy()
        if TOP in pure_keys:
            pure_keys.remove(TOP)
        if BOT in pure_keys:
            pure_keys.remove(BOT)
        return (
            ([TOP] if TOP in keys else [])
            + list(sorted(pure_keys))
            + ([BOT] if BOT in keys else [])
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
            + "$ & $".join([r"\cdot"] + self.symbols)
            + "$\\\\\\hline\n"
        )
        for row in self.symbols:
            table += "$" + row + "$ & "
            for col in self.symbols:
                table += "$" + self.mult[row][col] + "$"
                if col != BOT:
                    table += " & "
            if row != BOT:
                table += r"\\"
            table += "\n"
        table += "\\end{tabular}\n" + "\\end{table}\n"
        return table

    def mace4_format(self) -> str:
        """
        represent the binar in ``Prover9/Mace4`` format
        :returns: a string representation
        """
        self.remap_symbols(
            {value: str(key) for key, value in enumerate(self.symbols)}
        )
        result = ""
        for i in self.symbols:
            for j in self.symbols:
                result += f"{i} ^ {j} = {self.meet[i][j]}.\n"
                result += f"{i} v {j} = {self.join[i][j]}.\n"
                result += f"{i} \\ {j} = {self.undr[i][j]}.\n"
                result += f"{i} / {j} = {self.over[i][j]}.\n"
                result += f"{i} * {j} = {self.mult[i][j]}.\n"
        return result

    def _cayley_tabular_view(
        self, cayley_table: CayleyTable
    ) -> List[List[int]]:
        inverse_index = {symbol: i for i, symbol in enumerate(self.symbols)}
        table: List[List[int]] = []
        for one in self.symbols:
            table.append([])
            for two in self.symbols:
                table[inverse_index[one]].append(
                    inverse_index[cayley_table[one][two]]
                )
        return table

    def tabular_format(self) -> Dict[str, List[List[int]]]:
        """
        :returns: a dictionary of Cayley tables as lists of lists
        """
        return {
            "^": self._cayley_tabular_view(self.meet),
            "v": self._cayley_tabular_view(self.join),
            "*": self._cayley_tabular_view(self.mult),
            "\\": self._cayley_tabular_view(self.undr),
            "/": self._cayley_tabular_view(self.over),
        }


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
