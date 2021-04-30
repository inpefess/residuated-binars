# Distributivity Laws in Residuated Binars with Involution

This repo generates counter-examples for inter-relations between abstract distributivity laws in residuated binars with involution. For previous work in this field and more mathematical context see [Fussner, W., Jipsen, P. Distributive laws in residuated binars. Algebra Univers. 80, 54 (2019)](https://doi.org/10.1007/s00012-019-0625-1).

# Running this code

* an installation of [Isabelle proof assistant](https://isabelle.in.tum.de) is on the `$PATH`
* switch to Python 3.9 environment with `poetry` installed
* `poetry install` from the project's root
* `python residuated_binars/use_nitpick.py` or a similar command from another working directory

# Scripts descriptions

## `generate_theories.py`

Creates a folder with a specified name and fills it with valid Isabelle theory files. Each theory file contains only one lemma without a proof and does not depend on any other theories. The exact statement of lemmas is hard-coded. It may have the following assumptions:

* lattice axioms
* residuation axioms
* existence of the latest and the greatest elements of the lattice (they always exist in finite models)
* a definition of the involution operation
* some combination of abstract distributivity laws (from `ASSUMPTIONS` variable of `constants.py`)

The consequent of the lemma is one of the laws from `ASSUMPTIONS` which is not in the antecedent. So, if one has six laws in `ASSUMPTIONS` list, there will be `6 * (2 ^ 5 - 1) = 186` original hypotheses to check for models of different cardinalities.

The theory files are called `T[number].thy` where `number` enumerates theory files starting from zero.

## `add_task.py`

* for every theory file in a given folder
* creates a new file with the same name in another given folder
* the output file includes the same one lemma as the input
* but the 'task' is changed according to the script's parameters

Possible task types:
* `TaskType.NITPICK`, demands a `cardinality` to be provided as well (finite model search)
* `TaskType.SLEDGEHAMMER` (automated proof search)

Both task types have a hard-coded timeout of `1000000` seconds.

## `check_assumptions.py`

* gets all theory files from a given directory
* constructs a command for Isabelle server to process these files
* saves the log of Isabelle server replies to the file named `isabelle.out` in the directory where the theory files are

This script depends on [Python client for Isabelle server](https://pypi.org/project/isabelle-client).

## `filter_theories.py`

* reads from `isabelle.out` file from the input directory (this directory should be an output of `check_assumption.py` script)
* filters only those theory files, for which neither finite model was found, nor the proof (depending on the task type)
* copies filtered theory files from the input directory to another given directory

## `use_nitpick.py`

A wrapper 'do all' script.

* runs `generate_theories.py` which creates a new `hyp2` folder with initial hypotheses templates
* then for each cardinality from 2 to 100 (hard-coded)
* runs `add_task.py` which creates a `task[n]` folder for a particular cardinality with a respective task for `Nitpick` added to the templates in `hyp[n]`
* runs `check_assumptions.py` on a `task[n]` folder
* runs `filter_theories.py` which filter theories with no counter-examples found to a new folder `hyp[n+1]`
* if the `hyp[n+1]` folder is empty, the script stops (that means counter-examples were found for all original hypotheses)

# Other files

## `DistributiveCase.thy`

A human-written proof of one of the known statements about distributivity in residuated binars.

## `residuated_binar_to_tex.py`

A mostly hard-coded script which:

* gets `isabelle.out` files from some directories
* parses JSON replies from Isabelle server
* extracts the finite models found
* represents the models as Cayley tables (for semigroup reduct), Hasse diagrams (for a lattice reduct), and a table for involution operation
* the output is in `LaTeX` format using `tikz` package

This script depends on [dot2tex](https://pypi.org/project/dot2tex).
