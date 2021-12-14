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


class Lattice:
    r"""
        a representation of a lattice

    >>> lattice = Lattice(
    ...     label="test",
    ...     operations={
    ...         "join": {"0": {"0": "0", "1": "1"}, "1": {"0": "1", "1": "1"}},
    ...         "meet": {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "1"}},
    ...     }
    ... )
    >>> lattice.canonise_symbols()
    >>> sorted(lattice.more.items())
    [('⟘', []), ('⟙', ['⟘'])]
    >>> lattice.hasse
    [('⟙', '⟘')]
    >>> print(lattice.graphviz_repr)
    graph {
        "⟙" -- "⟘"
    }
    >>> print(lattice.mace4_format)
    0 ^ 0 = 0.
    0 v 0 = 0.
    0 ^ 1 = 1.
    0 v 1 = 0.
    1 ^ 0 = 1.
    1 v 0 = 0.
    1 ^ 1 = 1.
    1 v 1 = 1.
    <BLANKLINE>
    >>> print("this_is_a_test_case", lattice.tabular_format)
    this_is_a_test_case {'^': [[0, 1], [1, 1]], 'v': [[0, 0], [0, 1]]}
    """

    def __init__(
        self,
        label: str,
        operations: Dict[str, Dict[str, Any]],
    ):
        self.label = label
        self.join: CayleyTable = operations["join"]
        self.meet: CayleyTable = operations["meet"]

    @property
    def more(self) -> Dict[str, List[str]]:
        """
        :returns: some representation of a 'more' relation of a lattice reduct
            of the lattice
        """
        relation: Dict[str, List[str]] = {}
        for one in self.symbols:
            relation[one] = []
            for two in self.symbols:
                if self.meet[one][two] == two and one != two:
                    relation[one].append(two)
        return relation

    @property
    def hasse(self) -> List[Tuple[str, str]]:
        """
        :returns: some representation of a Hasse diagram of a lattice reduct of
            the lattice
        """
        more = {
            pair[0]: pair[1]
            for pair in sorted(
                self.more.items(),
                key=lambda key_value: -len(key_value[1]),
            )
        }
        hasse = []
        for higher in more:
            nearest = set(more[higher])
            for lower in more[higher]:
                nearest = nearest.difference(set(more[lower]))
            hasse += [(higher, neighbour) for neighbour in list(nearest)]
        return hasse

    @property
    def graphviz_repr(self) -> str:
        """
        :returns: a representation usable by ``graphviz`` of a Hasse diagram of
            a lattice reduct of the lattice
        """
        graph = graphviz.Graph()
        for pair in self.hasse:
            graph.edge(pair[0], pair[1])
        return graph

    @property
    def cardinality(self) -> int:
        """
        :returns: number of items in the lattice
        """
        return len(self.join)

    def canonise_symbols(self) -> None:
        """
        renumerate lattice's items in a canonical way
        """
        symbol_map = {
            pair[1]: pair[0]
            for pair in zip(
                [BOT]
                + [chr(ord("a") + i) for i in range(self.cardinality - 2)]
                + [TOP],
                [
                    key
                    for key, value in sorted(
                        self.more.items(),
                        key=lambda key_value: (
                            len(key_value[1]),
                            key_value[0],
                        ),
                    )
                ],
            )
        }
        self.remap_symbols(symbol_map)

    @property
    def binary_operations(self) -> List[str]:
        """
        :returns: a list of binary operation names existing in this algebraic
            structure
        """
        return ["meet", "join"]

    def remap_symbols(self, symbol_map: Dict[str, str]) -> None:
        """rename symbols in a given way"""
        for table_name in self.binary_operations:
            table = getattr(self, table_name)
            new_table: CayleyTable = {}
            for one in symbol_map.keys():
                new_table[symbol_map[one]] = {}
                for two in symbol_map.keys():
                    new_table[symbol_map[one]][symbol_map[two]] = symbol_map[
                        table[one][two]
                    ]
            setattr(self, table_name, new_table)

    @property
    def symbols(self) -> List[str]:
        """
        :returns: a list of symbols denoting items of a lattice
        """
        keys = list(self.join.keys())
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
    def mace4_format(self) -> str:
        """
        represent the lattice in ``Prover9/Mace4`` format
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
        }

    def __repr__(self):
        return str(self.tabular_format)
