..
  Copyright 2021-2022 Boris Shminke

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

|CircleCI|\ |codecov|\ |RTFD|

Generating Algebraic Structures with Isabelle
==============================================

If you're looking for a reproducible example for AITP 2021 paper, find it `here <https://residuated-binars.readthedocs.io/en/latest/aitp2021.html>`__.

This packages serves for generating and validating examples of different algebraic structures using `Isabelle proof assistant <https://isabelle.in.tum.de>`__.

.. _how-to-install:

How to Install
===============

-  make sure that an installation of Isabelle is on the ``$PATH``
-  ``git clone https://github.com/inpefess/residuated-binars.git``
-  switch to Python 3.7+ environment with ``poetry`` installed
-  ``poetry install`` from the project’s root

Alternatively, one can use Docker:

.. code:: sh

      docker build -t residuated-binars https://github.com/inpefess/residuated-binars.git
      docker run -it --rm -p 8888:8888 residuated-binars jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser

Finally, one can run it on
`Binder <https://mybinder.org/v2/gh/inpefess/residuated-binars/HEAD?labpath=reproduce-residuated-binars-papers.ipynb>`__


How to Use
===========

See ``examples/residuated-binars-example.ipynb``.

.. |CircleCI| image:: https://circleci.com/gh/inpefess/residuated-binars.svg?style=svg
   :target: https://circleci.com/gh/inpefess/residuated-binars
.. |codecov| image:: https://codecov.io/gh/inpefess/residuated-binars/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/inpefess/residuated-binars
.. |RTFD| image:: https://readthedocs.org/projects/residuated-binars/badge/?version=latest
   :target: https://residuated-binars.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
