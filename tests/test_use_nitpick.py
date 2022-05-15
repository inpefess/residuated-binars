"""
   Copyright 2021-2022 Boris Shminke

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import os
import shutil
import sys
from unittest import TestCase
from unittest.mock import Mock, patch

from residuated_binars.check_assumptions import check_assumptions
from residuated_binars.use_nitpick import use_nitpick

if sys.version_info.major == 3 and sys.version_info.minor >= 9:
    # pylint: disable=no-name-in-module
    from importlib.resources import files  # type: ignore
else:
    from importlib_resources import files  # pylint: disable=import-error


# pylint: disable=unused-argument
def mock_use_theories(**kwargs):
    """copy a ready file of Isabelle replies"""
    shutil.copyfile(
        files("residuated_binars").joinpath("resources/isabelle.out"),
        os.path.join("task2", "isabelle.out"),
    )


class TestUseNitpick(TestCase):
    """test ``use_nitpick`` function"""

    @patch("residuated_binars.check_assumptions.get_isabelle_client")
    @patch("residuated_binars.check_assumptions.start_isabelle_server")
    def test_use_nitpick(self, mock_server_start, mock_get_client):
        """test ``use_nitpick`` function"""
        mock_server_start.return_value = ("info", None)
        mock_client = Mock()
        mock_client.shutdown = lambda: 0
        mock_client.use_theories = mock_use_theories
        mock_get_client.return_value = mock_client
        for path in ["hyp2", "hyp3", "task2"]:
            shutil.rmtree(path, ignore_errors=True)
        use_nitpick(2, 6 * ["True"], [], True)
        check_assumptions("task2")
        self.assertEqual(len(os.listdir("hyp3")), 186)
