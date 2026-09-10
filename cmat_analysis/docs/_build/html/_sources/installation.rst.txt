Installation
============

From the repository root, install the library in editable mode::

   python -m pip install -e "./cmat_analysis[dev]"

For documentation development::

   python -m pip install -e "./cmat_analysis[docs]"
   sphinx-build -W -b html cmat_analysis/docs cmat_analysis/docs/_build/html

The ``src/`` layout is intentional; after installation use ``import
cmat_analysis`` rather than importing a nested package name.
