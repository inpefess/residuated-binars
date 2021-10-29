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
import json
import os
import re
import shutil
from argparse import ArgumentParser, Namespace
from typing import List, Optional


def filter_theories(source_path: str, target_path: str) -> None:
    """
    get theory files from an existing folder and copy to another existing
    folder ones those of them, for which neither have a finite counter-example
    nor a proof

    :param source_path: where to look for processed theory files; should
        include an ``isabelle.out`` file with server's output
    :param target_path: where to put theory files without proofs or
        counter-examples
    :returns:
    """
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    with open(
        os.path.join(source_path, "isabelle.out"), "r", encoding="utf-8"
    ) as out_file:
        final_line = [
            re.compile(".*FINISHED (.*)\n?").match(line)
            for line in out_file.readlines()
            if "FINISHED" in line
            and ("Sledgehammering" in line or "Nitpick" in line)
        ][0]
    if final_line is None:
        raise ValueError(f"Unexpected Isabelle server response: {final_line}")
    results = {
        node["theory_name"][6:]: [
            message["message"]
            for message in node["messages"]
            if "Try this: " in message["message"]
            or "Timed out" in message["message"]
            or "Nitpick found a potentially spurious counterexample"
            in message["message"]
            or "Nitpick found no counterexample" in message["message"]
        ][0]
        for node in json.loads(final_line.group(1))["nodes"]
    }
    for result in results:
        if (
            "Nitpick found no counterexample" in results[result]
            or "Timed out" in results[result]
        ):
            shutil.copy(
                os.path.join(source_path, result + ".thy"),
                os.path.join(target_path, result + ".thy"),
            )


def parse_args(args: Optional[List[str]] = None) -> Namespace:
    """
    >>> print(parse_args(["--source_path", "one", "--target_path", "two"])
    ...     .source_path)
    one

    :param args: a list of string arguments
        (for testing and use in a non script scenario)
    :returns: arguments namespace for the script
    """
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--source_path", type=str, required=True)
    argument_parser.add_argument("--target_path", type=str, required=True)
    parsed_args = argument_parser.parse_args(args)
    return parsed_args


if __name__ == "__main__":
    arguments = parse_args()
    filter_theories(arguments.source_path, arguments.target_path)
