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
# pylint: disable=all
import os
import shutil
import sys
from unittest import TestCase
from unittest.mock import Mock, patch

from residuated_binars.use_nitpick import parse_args, use_nitpick

if sys.version_info.major == 3 and sys.version_info.minor >= 9:
    from importlib.resources import files
else:
    from importlib_resources import files  # type: ignore


def mock_use_theories(folder, master_dir, watchdog_timeout):
    shutil.copyfile(
        files("residuated_binars").joinpath("resources/isabelle.out"),
        "task2/isabelle.out",
    )


class TestUseNitpick(TestCase):
    @patch("residuated_binars.check_assumptions.get_isabelle_client")
    @patch("residuated_binars.check_assumptions.start_isabelle_server")
    def test_use_nitpick(self, mock_server_start, mock_get_client):
        mock_server_start.return_value = ("info", None)
        mock_client = Mock()
        mock_client.shutdown = lambda: 0
        mock_client.use_theories = mock_use_theories
        mock_get_client.return_value = mock_client
        shutil.rmtree("hyp2", ignore_errors=True)
        shutil.rmtree("hyp3", ignore_errors=True)
        shutil.rmtree("task2", ignore_errors=True)
        use_nitpick(parse_args(["--max_cardinality", "2"]).max_cardinality)
        self.assertEqual(len(os.listdir("hyp3")), 186)
