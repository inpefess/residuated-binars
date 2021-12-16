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
    path: str,
    independent_assumptions: List[str],
    assumption_indices: List[int],
    goal_index: int,
    additional_assumptions: List[str],
) -> None:
    """
    generate a text of ``isabelle`` theory file for checking independence of
    one chosen assumpion from some subset of the rest

    :param path: a folder for storing theory files
    :param independent_assumptions: a list of assumption which independence
        we want to check
    :param assumption_indices: indices of assumption to use
    :param goal_index: index of a goal to prove
    :param additional_assumptions: a list of additional assumptions about
        the binars like the lattice reduct distributivity, existence of
        an involution operation, and multiplication associativity
    :returns:
    """
    assumption_list = list(assumption_indices)
    theory_name = f"T{''.join(map(str, assumption_list))}_{goal_index}"
    all_assumptions = [
        independent_assumptions[k] for k in assumption_indices
    ] + additional_assumptions
    theory_text = generate_isabelle_theory_file(
        theory_name,
        all_assumptions,
        independent_assumptions[goal_index],
    )
    with open(
        os.path.join(path, f"{theory_name}.thy"),
        "w",
        encoding="utf-8",
    ) as theory_file:
        theory_file.write("\n".join(theory_text))


def independence_check(
    path: str,
    independent_assumptions: List[str],
    additional_assumptions: List[str],
    check_subset_independence: bool,
) -> None:
    """
    generate a bunch of theory files to check independence of some assumptions
    given additional ones

    :param path: a folder for storing theory files
    :param independent_assumptions: a list of assumption which independence
        we want to check
    :param additional_assumptions: a list of additional assumptions
    :param check_subset_independence: whether to check every assumption from
        the list against all the rest or against any combination of the rest
    :returns:
    """
    if not os.path.exists(path):
        os.mkdir(path)
    total_assumptions_count = len(independent_assumptions)
    for goal_index in range(total_assumptions_count):
        for assumptions_count in range(1, total_assumptions_count):
            indices = tuple(
                list(range(0, goal_index))
                + list(range(goal_index + 1, total_assumptions_count))
            )
            if check_subset_independence:
                index_combinations = list(
                    combinations(
                        indices,
                        assumptions_count,
                    )
                )
            else:
                index_combinations = [indices]
            for assumption_indices in index_combinations:
                independence_case(
                    path,
                    independent_assumptions,
                    list(assumption_indices),
                    goal_index,
                    additional_assumptions,
                )
