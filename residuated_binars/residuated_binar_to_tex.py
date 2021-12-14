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
from residuated_binars.lattice import BOT, TOP
from residuated_binars.parser import isabelle_response_to_binar


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
        output_filename = f"task{i}/isabelle.out"
        models += isabelle_response_to_binar(output_filename)
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
        output_filename = f"task{i}/isabelle.out"
        models += isabelle_response_to_binar(output_filename)
    binars = [binar for binar in models if binar.label in {"T123"}]
    for binar in binars:
        print(binar.mace4_format())
        break


if __name__ == "__main__":
    generate_tex()
