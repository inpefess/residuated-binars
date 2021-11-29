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
from typing import Any, Dict, List, Tuple

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
    >>> binar.less
    {'⟙': [], '⟘': ['⟙']}
    >>> binar.hasse
    [('⟘', '⟙')]
    >>> print(binar.graphviz_repr)
    graph {
        "⟘" -- "⟙"
    }
    >>> print(binar.mace4_format)
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
    >>> print(binar.latex_mult_table)
    \begin{table}[]
    \begin{tabular}{l|ll}
    $\cdot$ & $0$ & $1$\\\hline
    $0$ & $1$ & $1$ & \\
    $1$ & $1$ & $1$ & \\
    \end{tabular}
    \end{table}
    <BLANKLINE>
    >>> print("this_is_a_test_case", binar.tabular_format)
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
        empty_dict: Dict[str, str] = {}
        self.invo: Dict[str, str] = operations.get("invo", empty_dict)

    @property
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

    @property
    def hasse(self) -> List[Tuple[str, str]]:
        """
        :returns: some representation of a Hasse diagram of a lattice reduct of
            the binar
        """
        less = {
            pair[0]: pair[1]
            for pair in sorted(
                self.less.items(),
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

    @property
    def graphviz_repr(self) -> str:
        """
        :returns: a representation usable by ``graphviz`` of a Hasse diagram of
            a lattice reduct of the binar
        """
        graph = graphviz.Graph()
        for pair in self.hasse:
            graph.edge(pair[0], pair[1])
        return graph

    @property
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
                + [chr(ord("a") + i) for i in range(self.cardinality - 2)]
                + [BOT],
                [
                    key
                    for key, value in sorted(
                        self.less.items(),
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
        if self.invo != {}:
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

    @property
    def latex_mult_table(self) -> str:
        """
        :returns: a LaTeX representation of a multiplication table
        """
        table = (
            "\\begin{table}[]\n"
            + "\\begin{tabular}"
            + f"{{l|{''.join((self.cardinality) * 'l')}}}\n"
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

    @property
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

    @property
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
