# Copyright 2021 Boris Shminke

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
Residuated Binar to TeX
========================

A mostly hard-coded script which:

-  gets ``isabelle.out`` files from some directories
-  parses JSON replies from Isabelle server
-  extracts the finite models found
-  represents the models as Cayley tables (for semigroup reduct), Hasse
   diagrams (for a lattice reduct), and a table for involution operation
-  the output is in ``LaTeX`` format using ``tikz`` package

This script depends on `Graphviz <https://graphviz.org/>`__.

"""
import os

from residuated_binars.lattice import BOT, TOP
from residuated_binars.parser import isabelle_response_to_algebra


def hard_coded_order(binars) -> None:
    """
    remap item names of all binars to have the same Hasse diagram

    :param binars: a list of some very specific binars
    :returns:
    """
    some_map = {
        c: c for c in [chr(ord("a") + i) for i in range(8)] + [TOP, BOT]
    }
    some_map.update({"f": "g", "g": "f"})
    binars[1].remap_symbols(some_map)
    binars[5].remap_symbols(some_map)
    some_map.update({"a": "b", "b": "a"})
    binars[2].remap_symbols(some_map)
    some_map.update({"d": "e", "e": "d"})
    binars[3].remap_symbols(some_map)
    binars[4].remap_symbols(some_map)


def generate_tex():
    """generate some TeX code"""
    models = []
    for i in [4, 7, 8, 10]:
        output_filename = os.path.join(f"task{i}", "isabelle.out")
        models += isabelle_response_to_algebra(output_filename)
    binars = [
        binar
        for binar in models
        if binar.label in {"T30", "T61", "T92", "T123", "T154", "T185"}
    ]
    for binar in binars:
        binar.canonise_symbols()
    hard_coded_order(binars)
    for binar in binars:
        print("%", binar.label)
        print(binar.latex_mult_table())
        binar.graphviz_repr().render(binar.label)


def generate_mace():
    """generate Mace4 input format"""
    models = []
    for i in [4, 7, 8, 10]:
        output_filename = os.path.join(f"task{i}", "isabelle.out")
        models += isabelle_response_to_algebra(output_filename)
    binars = [binar for binar in models if binar.label in {"T123"}]
    for binar in binars:
        print(binar.mace4_format())
        break


if __name__ == "__main__":
    generate_tex()
