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

from residuated_binars.add_task import TaskType, add_task
from residuated_binars.check_assumptions import check_assumptions
from residuated_binars.filter_theories import filter_theories
from residuated_binars.generate_theories import generate_theories


def use_nitpick():
    """
    incrementally search for finite counter-examples
    """
    cardinality = 2
    hypotheses = f"hyp{cardinality}"
    generate_theories(hypotheses)
    while cardinality <= 100 and os.listdir(hypotheses) != []:
        tasks = f"task{cardinality}"
        add_task(hypotheses, tasks, TaskType.NITPICK, cardinality)
        check_assumptions(tasks)
        cardinality += 1
        hypotheses = f"hyp{cardinality}"
        filter_theories(tasks, hypotheses)


if __name__ == "__main__":
    use_nitpick()
