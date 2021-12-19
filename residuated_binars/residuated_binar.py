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

from residuated_binars.axiom_checkers import (
    left_distributive,
    right_distributive,
)
from residuated_binars.lattice import BOT, Lattice


class ResiduatedBinar(Lattice):
    r"""
        a representation of a residuated binar (with involution)

    >>> join = {"0": {"0": "0", "1": "1"}, "1": {"0": "1", "1": "1"}}
    >>> meet = {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "1"}}
    >>> mult = {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "0"}}
    >>> const = {"0": {"0": "1", "1": "1"}, "1": {"0": "1", "1": "1"}}
    >>> binar = ResiduatedBinar(
    ...     label="test",
    ...     operations={
    ...         "join": join, "meet": meet, "mult": mult, "over": const,
    ...         "undr": const, "invo": {"0": "1", "1": "0"}
    ...     }
    ... )
    >>> print(binar.latex_mult_table)
    \begin{table}[]
    \begin{tabular}{l|ll}
    $\cdot$ & $0$ & $1$\\\hline
    $0$ & $0$ & $0$ & \\
    $1$ & $0$ & $0$ & \\
    \end{tabular}
    \end{table}
    <BLANKLINE>
    >>> print(binar.markdown_mult_table)
    |*|0|1|
    |-|-|-|
    |**0**|0|0|
    |**1**|0|0|
    <BLANKLINE>
    >>> mult["0"]["0"] = "1"
    >>> ResiduatedBinar("test", {"join": join, "meet": meet, "mult": mult,
    ...     "over": const, "undr": const})
    Traceback (most recent call last):
     ...
    ValueError: multiplication must be distributive over join
    >>> mult["0"]["0"] = "0"
    >>> const["0"]["0"] = "0"
    >>> ResiduatedBinar("test", {"join": join, "meet": meet, "mult": mult,
    ...     "over": const, "undr": const})
    Traceback (most recent call last):
     ...
    ValueError: check residuated binars axioms!
    >>> mult = {"0": {"0": "0", "1": "0"}, "1": {"0": "1", "1": "1"}}
    >>> undr = {"0": {"0": "1", "1": "1"}, "1": {"0": "0", "1": "1"}}
    >>> ResiduatedBinar("test", {"join": join, "meet": meet, "mult": mult,
    ...     "over": mult, "undr": undr})
    Traceback (most recent call last):
     ...
    ValueError: check residuated binars axioms!
    >>> print(binar.mace4_format[:10])
    0 v 0 = 0.
    """

    def check_axioms(self) -> None:
        super().check_axioms()
        if not left_distributive(
            self.operations["mult"], self.operations["join"]
        ) or not right_distributive(
            self.operations["mult"], self.operations["join"]
        ):
            raise ValueError("multiplication must be distributive over join")
        if not self._check_residuated_binars_axioms():
            raise ValueError("check residuated binars axioms!")

    def _check_residuated_binars_axioms(self) -> bool:
        for one in self.symbols:
            for two in self.symbols:
                if (
                    self.operations["join"][
                        self.operations["mult"][
                            self.operations["over"][one][two]
                        ][two]
                    ][one]
                    != one
                    or self.operations["join"][
                        self.operations["mult"][two][
                            self.operations["undr"][two][one]
                        ]
                    ][one]
                    != one
                ):
                    return False
                for three in self.symbols:
                    if (
                        self.operations["meet"][one][
                            self.operations["over"][
                                self.operations["join"][
                                    self.operations["mult"][one][two]
                                ][three]
                            ][two]
                        ]
                        != one
                        or self.operations["meet"][two][
                            self.operations["undr"][one][
                                self.operations["join"][
                                    self.operations["mult"][one][two]
                                ][three]
                            ]
                        ]
                        != two
                    ):
                        return False
        return True

    @property
    def operation_map(self) -> Dict[str, str]:
        res = super().operation_map
        res.update({"over": "/", "undr": "\\", "mult": "*"})
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
