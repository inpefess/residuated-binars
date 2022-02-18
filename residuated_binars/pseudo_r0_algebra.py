# Copyright 2022 Boris Shminke
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Pseudo R_0 Algebra
==================
"""
from residuated_binars.algebraic_structure import TOP
from residuated_binars.pseudo_weak_r0_algebra import PseudoWeakR0Algebra


class PseudoR0Algebra(PseudoWeakR0Algebra):
    r"""
    a representation of a peudo R_0 algebra
    """

    def check_axioms(self) -> None:
        super().check_axioms()
        message = "P5 axiom doesn't hold"
        for one in self.operations["meet"].keys():
            for two in self.operations["meet"].keys():
                assert (
                    self.operations["join"][self.operations["imp1"][one][two]][
                        self.operations["imp2"][
                            self.operations["imp1"][one][two]
                        ][
                            self.operations["join"][
                                self.operations["inv1"][one]
                            ][two]
                        ]
                    ]
                    == TOP
                ), message
                assert (
                    self.operations["join"][self.operations["imp2"][one][two]][
                        self.operations["imp1"][
                            self.operations["imp2"][one][two]
                        ][
                            self.operations["join"][
                                self.operations["inv2"][one]
                            ][two]
                        ]
                    ]
                    == TOP
                ), message
