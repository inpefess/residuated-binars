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
import logging
import os
from argparse import ArgumentParser, Namespace
from typing import List, Optional

import nest_asyncio
from isabelle_client import get_isabelle_client
from isabelle_client.utils import start_isabelle_server


def get_customised_logger(task_folder: str) -> logging.Logger:
    """
    get a nice logger

    :param rask_folder: a base folder (and a task name)
    """
    logfile_name = os.path.join(task_folder, "isabelle.out")
    if os.path.exists(logfile_name):
        os.remove(logfile_name)
    logger = logging.getLogger(os.path.basename(task_folder))
    handler = logging.FileHandler(logfile_name)
    handler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def check_assumptions(path: str) -> None:
    """
    ask Isabelle server to process all theory files in a given path

    :param path: a folder with theory files
    :returns:
    """
    nest_asyncio.apply()
    theories = [
        theory_name[0]
        for theory_name in [
            os.path.splitext(theory_file) for theory_file in os.listdir(path)
        ]
        if theory_name[1] == ".thy"
    ]
    server_info, _ = start_isabelle_server(
        log_file=os.path.join(path, "server.log"), name=os.path.basename(path)
    )
    isabelle_client = get_isabelle_client(server_info)
    isabelle_client.logger = get_customised_logger(path)
    isabelle_client.use_theories(
        theories, master_dir=os.path.abspath(path), watchdog_timeout=0
    )
    isabelle_client.shutdown()


def parse_args(args: Optional[List[str]] = None) -> Namespace:
    """
    >>> print(parse_args(["--path", "one"]).path)
    one

    :param args: a list of string arguments
        (for testing and use in a non script scenario)
    :returns: arguments namespace for the script
    """
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--path", type=str, required=True)
    return argument_parser.parse_args(args)


if __name__ == "__main__":
    arguments = parse_args()
    check_assumptions(arguments.path)
