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
from typing import List, Optional

from residuated_binars.add_task import TaskType, add_task
from residuated_binars.check_assumptions import check_assumptions
from residuated_binars.filter_theories import filter_theories
from residuated_binars.generate_theories import generate_theories


def use_nitpick(max_cardinality: int):
    """
    incrementally search for finite counter-examples

    :param max_cardinality: maximal cardinality of a model to search for
    """
    cardinality = 2
    hypotheses = f"hyp{cardinality}"
    generate_theories(hypotheses)
    while cardinality <= max_cardinality and os.listdir(hypotheses) != []:
        tasks = f"task{cardinality}"
        add_task(hypotheses, tasks, TaskType.NITPICK, cardinality)
        check_assumptions(tasks)
        cardinality += 1
        hypotheses = f"hyp{cardinality}"
        filter_theories(tasks, hypotheses)


def parse_args(args: Optional[List[str]] = None) -> Namespace:
    """

    :param args: a list of string arguments
        (for testing and use in a non script scenario)
    :returns: arguments namespace for the script
    """
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--max_cardinality", type=int, required=True)
    parsed_args = argument_parser.parse_args(args)
    return parsed_args


if __name__ == "__main__":
    use_nitpick(parse_args().max_cardinality)
