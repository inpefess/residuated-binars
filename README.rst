|CircleCI|\ |codecov|

Distributivity Laws in Residuated Binars with Involution
========================================================

This repo generates counter-examples for inter-relations between
abstract distributivity laws in residuated binars with involution.

If you would like to listen to a talk about this work, see `6th
Conference on Artificial Intelligence and Theorem
Proving <http://grid01.ciirc.cvut.cz/~mptp/zoomaitp/2021-09-06a/zoom_0.mp4>`__

If you would like to cite this work, use `arXiv
preprint <https://arxiv.org/abs/2109.05264>`__.

For previous work in this field and more mathematical context see
`Fussner, W., Jipsen, P. Distributive laws in residuated binars. Algebra
Univers. 80, 54 (2019) <https://doi.org/10.1007/s00012-019-0625-1>`__.

``notebooks/rb-check.ipynb`` file is a contribution of `Carlos
Simpson <https://github.com/carlostsimpson>`__.

Running this code
=================

-  an installation of `Isabelle proof
   assistant <https://isabelle.in.tum.de>`__ is on the ``$PATH``
-  switch to Python 3.9 environment with ``poetry`` installed
-  ``poetry install`` from the project’s root
-  ``python residuated_binars/use_nitpick.py`` or a similar command from
   another working directory

Alternatively, one can use Docker:

.. code:: sh

      docker build -t residuated-binars https://github.com/inpefess/residuated-binars.git
      docker run -it --rm -p 8888:8888 residuated-binars jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser

and then navigate to ``residuated-binars-example.ipynb``.

Finally, one can run it on
`Binder <https://mybinder.org/v2/gh/inpefess/residuated-binars/HEAD?labpath=residuated-binars-example.ipynb>`__


Files descriptions
===================

``DistributiveCase.thy``
------------------------

A human-written proof of one of the known statements about
distributivity in residuated binars.

``notebooks/binars.pkl``
------------------------

A serialisation of tabular representation of six binars having some
particular properties. Can be obtained using
``residuated_binar_to_tex.py``

``notebooks/rb-check.ipynb``
----------------------------

A file for checking algebraic properties of ``binars.pkl``

``notebooks/another-check.ipynb``
---------------------------------

Another file for checking algebraic properties of ``binars.pkl``

.. |CircleCI| image:: https://circleci.com/gh/inpefess/residuated-binars.svg?style=svg
   :target: https://circleci.com/gh/inpefess/residuated-binars
.. |codecov| image:: https://codecov.io/gh/inpefess/residuated-binars/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/inpefess/residuated-binars
