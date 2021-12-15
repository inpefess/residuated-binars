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
from typing import Dict

from residuated_binars.lattice import BOT, Lattice


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
    >>> print(binar.mace4_format)
    0 v 0 = 0.
    0 v 1 = 1.
    1 v 0 = 1.
    1 v 1 = 1.
    0 ^ 0 = 0.
    0 ^ 1 = 0.
    1 ^ 0 = 0.
    1 ^ 1 = 1.
    0 * 0 = 0.
    0 * 1 = 0.
    1 * 0 = 0.
    1 * 1 = 0.
    0 \ 0 = 1.
    0 \ 1 = 1.
    1 \ 0 = 1.
    1 \ 1 = 1.
    0 / 0 = 1.
    0 / 1 = 1.
    1 / 0 = 1.
    1 / 1 = 1.
    invo(0) = 1.
    invo(1) = 0.
    <BLANKLINE>
    >>> binar.canonise_symbols()
    >>> sorted(binar.more.items())
    [('⟘', []), ('⟙', ['⟘'])]
    >>> binar.hasse
    [('⟙', '⟘')]
    >>> print(binar.graphviz_repr)
    graph {
        "⟙" -- "⟘"
    }
    >>> print(binar.latex_mult_table)
    \begin{table}[]
    \begin{tabular}{l|ll}
    $\cdot$ & $⟘$ & $⟙$\\\hline
    $⟘$ & $⟘$$⟘$ &
    $⟙$ & $⟘$$⟘$ & \\
    \end{tabular}
    \end{table}
    <BLANKLINE>
    >>> print(binar.markdown_mult_table)
    |*|⟘|⟙|
    |-|-|-|
    |**⟘**|⟘|⟘|
    |**⟙**|⟘|⟘|
    >>> print("this_is_a_test_case", binar)
    this_is_a_test_case {'join': [[0, 1], [1, 1]], 'meet': [[0, 0], [0, 1]], 'mult': [[0, 0], [0, 0]], 'over': [[1, 1], [1, 1]], 'undr': [[1, 1], [1, 1]], 'invo': [1, 0]}
    """

    @property
    def operation_map(self) -> Dict[str, str]:
        res = super().operation_map
        res.update({"over": "\\", "undr": "/", "mult": "*"})
        return res

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
                table += "$" + self.operations["mult"][row][col] + "$"
                if col != BOT:
                    table += " & "
            if row != BOT:
                table += r"\\"
            table += "\n"
        table += "\\end{tabular}\n" + "\\end{table}\n"
        return table

    @property
    def markdown_mult_table(self) -> str:
        """
        :returns: a Markdown representation of a multiplication table
        """
        table = "|*|" + "|".join(self.symbols) + "|\n"
        table += "|" + (1 + len(self.symbols)) * "-|" + "\n"
        for row in self.symbols:
            table += "|**" + row + "**|"
            for col in self.symbols:
                table += self.operations["mult"][row][col] + "|"
            table += "\n"
        return table
