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
import os
from argparse import ArgumentParser, Namespace
from itertools import combinations
from typing import List, Optional

from residuated_binars.constants import (
    ASSUMPTIONS,
    BOUNDED_LATTICE,
    INVOLUTION,
    RESIDUATED_BINAR,
)


def get_isabelle_theory(
    theory_name: str,
    assumption_indices: List[int],
    goal_index: int,
) -> List[str]:
    """
    generate a text of ``isabelle`` theory file

    :param theory_name: name of a theory file
    :param assumption_indices: indices of assumption to use
    :param goal_index: index of a goal to prove
    :returns: a list of lines of a theory file
    """
    theory_text = [f"theory {theory_name}"]
    theory_text += ["imports Main", "begin", 'lemma "(']
    all_assumptions = (
        RESIDUATED_BINAR
        + BOUNDED_LATTICE
        + INVOLUTION
        + [ASSUMPTIONS[k] for k in assumption_indices]
    )
    theory_text += [" &\n".join(all_assumptions)]
    theory_text += [") \\<longrightarrow>"]
    theory_text += [ASSUMPTIONS[goal_index]]
    theory_text += ['"', "oops", "end"]
    return theory_text


def generate_theories(path: str) -> None:
    """
    generate a bunch of initial theories to check

    :param path: a folder for storing initial theories to check
    :returns:
    """
    if not os.path.exists(path):
        os.mkdir(path)
    total_assumptions_count = len(ASSUMPTIONS)
    theory_number = 0
    for goal_index in range(total_assumptions_count):
        for assumptions_count in range(1, total_assumptions_count):
            for assumption_indices in combinations(
                list(range(0, goal_index))
                + list(range(goal_index + 1, total_assumptions_count)),
                assumptions_count,
            ):
                lines = get_isabelle_theory(
                    f"T{theory_number}", list(assumption_indices), goal_index
                )
                with open(
                    os.path.join(path, f"T{theory_number}.thy"),
                    "w",
                    encoding="utf-8",
                ) as theory_file:
                    theory_file.write("\n".join(lines))
                theory_number += 1


def parse_args(args: Optional[List[str]] = None) -> Namespace:
    """

    :param args: a list of string arguments
        (for testing and use in a non script scenario)
    :returns: arguments namespace for the script
    """
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--path", type=str, required=True)
    parsed_args = argument_parser.parse_args(args)
    return parsed_args


if __name__ == "__main__":
    arguments = parse_args()
    generate_theories(arguments.path)
