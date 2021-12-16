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
from itertools import combinations
from typing import List, Optional


def generate_isabelle_theory_file(
    theory_name: str, assumptions: List[str], goal: Optional[str] = None
) -> List[str]:
    """
    generate a text of Isabelle theory file with only ones lemma inside

    :param theory_name: name of a theory file
    :param assumptions: a list of lemma assumptions in Isabelle language
    :param goal: the lemma goal in Isabelle language
    :returns: a list of lines of a theory file
    """
    theory_text = [f"theory {theory_name}"]
    theory_text += ["imports Main", "begin", 'lemma "(']
    theory_text += [" &\n".join(assumptions)]
    if goal is not None:
        theory_text += [") \\<longrightarrow>"]
        theory_text += [goal]
    else:
        theory_text += [")"]
    theory_text += ['"', "oops", "end"]
    return theory_text


def independence_case(
    theory_name: str,
    independent_assumptions: List[str],
    assumption_indices: List[int],
    goal_index: int,
    additional_assumptions: List[str],
) -> List[str]:
    """
    generate a text of ``isabelle`` theory file for checking independence of
    one chosen non-trivial distributivity law in residuated binars from all the
    others

    :param theory_name: name of a theory file
    :param independent_assumptions: a list of assumption which independence
        we want to check
    :param assumption_indices: indices of assumption to use
    :param goal_index: index of a goal to prove
    :param additional_assumptions: a list of additional assumptions about
        the binars like the lattice reduct distributivity, existence of
        an involution operation, and multiplication associativity
    :returns: a list of lines of a theory file
    """
    all_assumptions = [
        independent_assumptions[k] for k in assumption_indices
    ] + additional_assumptions
    theory_text = generate_isabelle_theory_file(
        theory_name,
        all_assumptions,
        independent_assumptions[goal_index],
    )
    return theory_text


def independence_check(
    path: str,
    independent_assumptions: List[str],
    additional_assumptions: List[str],
) -> None:
    """
    generate a bunch of theory files to check independence of some assumptions
    given additional ones

    :param path: a folder for storing theory files
    :param independent_assumptions: a list of assumption which independence
        we want to check
    :param additional_assumptions: a list of additional assumptions
    :returns:
    """
    if not os.path.exists(path):
        os.mkdir(path)
    total_assumptions_count = len(independent_assumptions)
    for goal_index in range(total_assumptions_count):
        for assumptions_count in range(1, total_assumptions_count):
            for assumption_indices in combinations(
                list(range(0, goal_index))
                + list(range(goal_index + 1, total_assumptions_count)),
                assumptions_count,
            ):
                assumption_list = list(assumption_indices)
                theory_name = (
                    f"T{''.join(map(str, assumption_list))}_{goal_index}"
                )
                lines = independence_case(
                    theory_name,
                    independent_assumptions,
                    assumption_list,
                    goal_index,
                    additional_assumptions,
                )
                with open(
                    os.path.join(path, f"{theory_name}.thy"),
                    "w",
                    encoding="utf-8",
                ) as theory_file:
                    theory_file.write("\n".join(lines))
