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
from typing import Dict

from residuated_binars.algebraic_structure import CayleyTable


def associative(cayley_table: CayleyTable) -> bool:
    """
    >>> associative({"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "0"}})
    True
    >>> associative({"0": {"0": "1", "1": "0"}, "1": {"0": "0", "1": "0"}})
    False

    :param cayley_table: a multiplication table of a binary operation
    :returns: whether the operation is associative or not
    """
    for one in cayley_table.keys():
        for two in cayley_table.keys():
            for three in cayley_table.keys():
                if (
                    cayley_table[one][cayley_table[two][three]]
                    != cayley_table[cayley_table[one][two]][three]
                ):
                    return False
    return True


def is_left_identity(cayley_table: CayleyTable, identity: str) -> bool:
    """
    >>> is_left_identity(
    ...     {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "1"}}, "1"
    ... )
    True
    >>> is_left_identity(
    ...     {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "1"}}, "0"
    ... )
    False

    :param cayley_table: a multiplication table of a binary operation
    :returns: whether ``identity`` is a left identity for a Cayley table
    """
    for one in cayley_table.keys():
        if cayley_table[identity][one] != one:
            return False
    return True


def is_right_identity(cayley_table: CayleyTable, identity: str) -> bool:
    """
    >>> is_right_identity(
    ...     {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "1"}}, "1"
    ... )
    True
    >>> is_right_identity(
    ...     {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "1"}}, "0"
    ... )
    False

    :param cayley_table: a multiplication table of a binary operation
    :returns: whether ``identity`` is a right identity for a Cayley table
    """
    for one in cayley_table.keys():
        if cayley_table[one][identity] != one:
            return False
    return True


def is_left_inverse(
    cayley_table: CayleyTable, inverse: Dict[str, str], identity: str
) -> bool:
    """
    >>> op = {"0": {"0": "1", "1": "1"}, "1": {"0": "1", "1": "1"}}
    >>> inv = {"0": "1", "1": "1"}
    >>> is_left_inverse(op, inv, "1")
    True
    >>> is_left_inverse(op, inv, "0")
    False

    :param cayley_table: a multiplication table of a binary operation
    :returns: whether ``inverse`` is a left inverse for a Cayley table
    """
    for one in cayley_table.keys():
        if cayley_table[inverse[one]][one] != identity:
            return False
    return True


def is_right_inverse(
    cayley_table: CayleyTable, inverse: Dict[str, str], identity: str
) -> bool:
    """
    >>> op = {"0": {"0": "1", "1": "1"}, "1": {"0": "1", "1": "1"}}
    >>> inv = {"0": "1", "1": "1"}
    >>> is_right_inverse(op, inv, "1")
    True
    >>> is_right_inverse(op, inv, "0")
    False

    :param cayley_table: a multiplication table of a binary operation
    :returns: whether ``inverse`` is a right inverse for a Cayley table
    """
    for one in cayley_table.keys():
        if cayley_table[one][inverse[one]] != identity:
            return False
    return True


def commutative(cayley_table: CayleyTable) -> bool:
    """
    >>> commutative({"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "0"}})
    True
    >>> commutative({"0": {"0": "0", "1": "1"}, "1": {"0": "0", "1": "0"}})
    False

    :param cayley_table: a multiplication table of a binary operation
    :returns: whether the operation is commutative or not
    """
    for one in cayley_table.keys():
        for two in cayley_table.keys():
            if cayley_table[one][two] != cayley_table[two][one]:
                return False
    return True


def idempotent(cayley_table: CayleyTable) -> bool:
    """
    >>> idempotent({"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "1"}})
    True
    >>> idempotent({"0": {"0": "0", "1": "1"}, "1": {"0": "0", "1": "0"}})
    False

    :param cayley_table: a multiplication table of a binary operation
    :returns: whether the operation is idempotent or not
    """
    for one in cayley_table.keys():
        if cayley_table[one][one] != one:
            return False
    return True


def left_distributive(table1: CayleyTable, table2: CayleyTable) -> bool:
    """
    >>> operation = {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "0"}}
    >>> left_distributive(operation, operation)
    True
    >>> operation = {"0": {"0": "1", "1": "0"}, "1": {"0": "0", "1": "0"}}
    >>> left_distributive(operation, operation)
    False

    :param table1: a multiplication table of a binary operation
    :param table2: a multiplication table of another binary operation
    :returns: whether the first operation is left distributive with respect to
        the second one or not
    """
    for one in table1.keys():
        for two in table1.keys():
            for three in table1.keys():
                if (
                    table1[one][table2[two][three]]
                    != table2[table1[one][two]][table1[one][three]]
                ):
                    return False
    return True


def right_distributive(table1: CayleyTable, table2: CayleyTable) -> bool:
    """
    >>> operation = {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "0"}}
    >>> right_distributive(operation, operation)
    True
    >>> operation = {"0": {"0": "0", "1": "1"}, "1": {"0": "0", "1": "0"}}
    >>> right_distributive(operation, operation)
    False

    :param table1: a multiplication table of a binary operation
    :param table2: a multiplication table of another binary operation
    :returns: whether the first operation is right distributive with respect to
        the second one or not
    """
    for one in table1.keys():
        for two in table1.keys():
            for three in table1.keys():
                if (
                    table1[table2[one][two]][three]
                    != table2[table1[one][three]][table1[two][three]]
                ):
                    return False
    return True


def absorbs(table1: CayleyTable, table2: CayleyTable) -> bool:
    """
    >>> conjuction = {"0": {"0": "0", "1": "0"}, "1": {"0": "0", "1": "1"}}
    >>> disjunction = {"0": {"0": "0", "1": "1"}, "1": {"0": "1", "1": "1"}}
    >>> absorbs(conjuction, disjunction)
    True
    >>> absorbs(conjuction, conjuction)
    False

    :param table1: a multiplication table of a binary operation
    :param table2: a multiplication table of another binary operation
    :returns: whether the absorption law is true with respect to
        two binary operation
    """
    for one in table1.keys():
        for two in table1.keys():
            if table1[one][table2[one][two]] != one:
                return False
    return True
