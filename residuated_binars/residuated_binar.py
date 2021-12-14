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
from typing import Any, Dict, List

from residuated_binars.lattice import BOT, CayleyTable, Lattice


class ResiduatedBinar(Lattice):
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
    >>> sorted(binar.more.items())
    [('⟘', []), ('⟙', ['⟘'])]
    >>> binar.hasse
    [('⟙', '⟘')]
    >>> print(binar.graphviz_repr)
    graph {
        "⟙" -- "⟘"
    }
    >>> print(binar.mace4_format)
    0 ^ 0 = 0.
    0 v 0 = 0.
    0 ^ 1 = 1.
    0 v 1 = 0.
    1 ^ 0 = 1.
    1 v 0 = 0.
    1 ^ 1 = 1.
    1 v 1 = 1.
    0 \ 0 = 0.
    0 / 0 = 0.
    0 * 0 = 1.
    0 \ 1 = 0.
    0 / 1 = 0.
    0 * 1 = 1.
    1 \ 0 = 0.
    1 / 0 = 0.
    1 * 0 = 1.
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
        super().__init__(label, operations)
        self.mult: CayleyTable = operations["mult"]
        self.over: CayleyTable = operations["over"]
        self.undr: CayleyTable = operations["undr"]
        empty_dict: Dict[str, str] = {}
        self.invo: Dict[str, str] = operations.get("invo", empty_dict)

    def remap_symbols(self, symbol_map: Dict[str, str]) -> None:
        """rename symbols in a given way"""
        super().remap_symbols(symbol_map)
        new_invo: Dict[str, str] = {}
        if self.invo != {}:
            for one in symbol_map.keys():
                new_invo[symbol_map[one]] = symbol_map[self.invo[one]]
        self.invo = new_invo

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
    def binary_operations(self) -> List[str]:
        """
        :returns: a list of binary operation names existing in this algebraic
            structure
        """
        return super().binary_operations + ["mult", "over", "undr"]

    @property
    def mace4_format(self) -> str:
        """
        represent the binar in ``Prover9/Mace4`` format
        :returns: a string representation
        """
        self.remap_symbols(
            {value: str(key) for key, value in enumerate(self.symbols)}
        )
        result = super().mace4_format
        for i in self.symbols:
            for j in self.symbols:
                result += f"{i} \\ {j} = {self.undr[i][j]}.\n"
                result += f"{i} / {j} = {self.over[i][j]}.\n"
                result += f"{i} * {j} = {self.mult[i][j]}.\n"
        return result

    @property
    def tabular_format(self) -> Dict[str, List[List[int]]]:
        """
        :returns: a dictionary of Cayley tables as lists of lists
        """
        res = super().tabular_format
        res.update(
            {
                "*": self._cayley_tabular_view(self.mult),
                "\\": self._cayley_tabular_view(self.undr),
                "/": self._cayley_tabular_view(self.over),
            }
        )
        return res
