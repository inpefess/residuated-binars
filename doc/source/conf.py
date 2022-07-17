# Copyright 2021-2022 Boris Shminke

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))
# pylint: disable=invalid-name
project = "residuated-binars"
# pylint: disable=invalid-name,redefined-builtin
copyright = "2021-2022, Boris Shminke"
author = "Boris Shminke"
release = "0.0.2"
extensions = ["sphinx.ext.autodoc"]
html_theme = "sphinx_rtd_theme"
