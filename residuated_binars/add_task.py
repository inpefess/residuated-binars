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
import re
from argparse import ArgumentParser, Namespace
from enum import Enum
from typing import List, Optional


class TaskType(Enum):
    """
    type of tasks to ask ``isabelle`` server to perform
    """

    SLEDGEHAMMER = "sledgehammer[timeout=1000000]"
    NITPICK = "nitpick[card nat=cardinality,timeout=1000000,max_threads=0]"


def add_task(
    source_path: str,
    target_path: str,
    task_type: TaskType,
    cardinality: int = 1,
) -> None:
    """
    take theory files from an existing folder and change tasks in them to given
    ones

    :param source_path: a directory where to get theory files to add tasks to
    :param target_path: where to put new theory files with added tasks
    :param task_type: use Nitpick or Sledgehammer (disprove by finding a finite
        coutner-example or prove)
    :param cardinality: a cardinality of finite model to find (only for Nitpick
        tasks)
    :returns:
    """
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    for theory_name in os.listdir(source_path):
        with open(os.path.join(source_path, theory_name), "r") as theory_file:
            theory_text = theory_file.read()
        theory_text = re.sub(
            "cardinality",
            str(cardinality),
            re.sub(
                '"\n.*\n?oops',
                '"\n' + task_type.value + "\noops",
                theory_text,
            ),
        )
        with open(os.path.join(target_path, theory_name), "w") as theory_file:
            theory_file.write(theory_text)


def parse_args(args: Optional[List[str]] = None) -> Namespace:
    """

    :param args: a list of string arguments
        (for testing and use in a non script scenario)
    :returns: arguments namespace for the script
    """
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--source_path", type=str, required=True)
    argument_parser.add_argument("--target_path", type=str, required=True)
    argument_parser.add_argument(
        "--task_type",
        type=str,
        choices=[TaskType.NITPICK.name, TaskType.SLEDGEHAMMER.name],
        required=True,
    )
    argument_parser.add_argument("--cardinality", type=int, required=False)
    parsed_args = argument_parser.parse_args(args)
    return parsed_args


if __name__ == "__main__":
    arguments = parse_args()
    add_task(
        arguments.source_path,
        arguments.target_path,
        TaskType.NITPICK
        if arguments.task_type == TaskType.NITPICK.name
        else TaskType.SLEDGEHAMMER,
        arguments.cardinality,
    )
