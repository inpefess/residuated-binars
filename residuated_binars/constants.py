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
Constants
==========
"""
FOR_X_Y = "\\<forall> x::nat. \\<forall> y::nat."
FOR_X_Y_Z = f"{FOR_X_Y} \\<forall> z::nat."
COMMUTATIVITY = f"({FOR_X_Y} f(x, y) = f(y, x))"
ASSOCIATIVITY = f"({FOR_X_Y_Z} f(x, f(y, z)) = f(f(x, y), z))"
IDEMPOTENCE = "(\\<forall> x::nat. f(x, x) = x)"
LEFT_IDENTITY = "(\\<forall> x::nat. f(1, x) = x)"
RIGHT_IDENTITY = "(\\<forall> x::nat. f(x, 1) = x)"
LEFT_ZERO = "(\\<forall> x::nat. f(0, x) = 0)"
RIGHT_ZERO = "(\\<forall> x::nat. f(x, 0) = 0)"
LEFT_DISTRIBUTIVITY = f"({FOR_X_Y_Z} f(x, g(y, z)) = g(f(x, y), f(x, z)))"
RIGHT_DISTRIBUTIVITY = f"({FOR_X_Y_Z} f(g(x, y), z) = g(f(x, z), f(y, z)))"
LEFT_ANTI_DISTRIBUTIVITY = f"({FOR_X_Y_Z} f(x, g(y, z)) = h(f(x, y), f(x, z)))"
RIGHT_ANTI_DISTRIBUTIVITY = (
    f"({FOR_X_Y_Z} f(g(x, y), z) = h(f(x, z), f(y, z)))"
)
PROJECTION = "(\\<forall> x::nat. f(f(x)) = x)"
DE_MORGAN = f"({FOR_X_Y} f(g(x, y)) = h(f(x), f(y)))"
ABSORPTION = f"({FOR_X_Y} f(x, g(x, y)) = x)"

LATTICE = [
    COMMUTATIVITY.replace("f(", "meet("),
    COMMUTATIVITY.replace("f(", "join("),
    ASSOCIATIVITY.replace("f(", "meet("),
    ASSOCIATIVITY.replace("f(", "join("),
    ABSORPTION.replace("f(", "meet(").replace("g(", "join("),
    ABSORPTION.replace("g(", "meet(").replace("f(", "join("),
]

RESIDUATED_BINAR = LATTICE + [
    LEFT_DISTRIBUTIVITY.replace("f(", "mult(").replace("g(", "join("),
    RIGHT_DISTRIBUTIVITY.replace("f(", "mult(").replace("g(", "join("),
    f"({FOR_X_Y_Z} meet(x, over(join(mult(x, y), z), y)) = x)",
    f"({FOR_X_Y_Z} meet(y, undr(x, join(mult(x, y), z))) = y)",
    f"({FOR_X_Y_Z} join(mult(over(x, y), y), x) = x)",
    f"({FOR_X_Y_Z} join(mult(y, undr(y, x)), x) = x)",
]

TRIVIAL_DISTRIBUTIVITY_LAWS = [
    LEFT_DISTRIBUTIVITY.replace("f(", "mult(").replace("g(", "join("),
    RIGHT_DISTRIBUTIVITY.replace("f(", "mult(").replace("g(", "join("),
    LEFT_DISTRIBUTIVITY.replace("f(", "undr(").replace("g(", "meet("),
    RIGHT_DISTRIBUTIVITY.replace("f(", "over(").replace("g(", "meet("),
    LEFT_ANTI_DISTRIBUTIVITY.replace("f(", "over(")
    .replace("g(", "join(")
    .replace("h(", "meet("),
    RIGHT_ANTI_DISTRIBUTIVITY.replace("f(", "undr(")
    .replace("g(", "join(")
    .replace("h(", "meet("),
]

BOUNDED_LATTICE = [
    LEFT_ZERO.replace("f(", "meet("),
    LEFT_IDENTITY.replace("f(", "meet("),
    RIGHT_ZERO.replace("f(", "meet("),
    RIGHT_IDENTITY.replace("f(", "meet("),
    LEFT_ZERO.replace("f(", "join(").replace("0", "1"),
    LEFT_IDENTITY.replace("f(", "join(").replace("1", "0"),
    RIGHT_ZERO.replace("f(", "join(").replace("0", "1"),
    RIGHT_IDENTITY.replace("f(", "join(").replace("1", "0"),
]

ORTHOCOMPLEMENTATION = [
    "(\\<forall> x::nat. meet(invo(x), x) = 0)",
    "(\\<forall> x::nat. join(invo(x), x) = 1)",
]

NON_TRIVIAL_DISTRIBUTIVITY_LAWS = [
    LEFT_DISTRIBUTIVITY.replace("f(", "mult(").replace("g(", "meet("),
    RIGHT_DISTRIBUTIVITY.replace("f(", "mult(").replace("g(", "meet("),
    LEFT_DISTRIBUTIVITY.replace("f(", "undr(").replace("g(", "join("),
    RIGHT_DISTRIBUTIVITY.replace("f(", "over(").replace("g(", "join("),
    LEFT_ANTI_DISTRIBUTIVITY.replace("f(", "over(")
    .replace("g(", "meet(")
    .replace("h(", "join("),
    RIGHT_ANTI_DISTRIBUTIVITY.replace("f(", "undr(")
    .replace("g(", "meet(")
    .replace("h(", "join("),
]

MODULARITY = (
    f"({FOR_X_Y_Z} f(g(x, z), g(y, z)) = g(f(g(x, z), y), z))".replace(
        "f(", "join("
    ).replace("g(", "meet(")
)

INVOLUTION = [
    DE_MORGAN.replace("f(", "invo(")
    .replace("g(", "join(")
    .replace("h(", "meet("),
    DE_MORGAN.replace("f(", "invo(")
    .replace("h(", "join(")
    .replace("g(", "meet("),
    PROJECTION.replace("f(", "invo("),
]

LEFT_INVERSE = "(\\<forall> x::nat. f(g(x), x) = 1)"
RIGHT_INVERSE = "(\\<forall> x::nat. f(x, g(x)) = 1)"
