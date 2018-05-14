conff
=====

Simple config parser with evaluator library.

`conff <https://pypi.org/pypi/conff/>`__
`Build Status <https://travis-ci.com/kororo/conff>`__
`Coverage Status <https://coveralls.io/github/kororo/conff?branch=master>`__
`Maintainability <https://codeclimate.com/github/kororo/conff/maintainability>`__

Why Another Config Parser Module?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This project started because of the complexity of project config. It
needs:
- import mechanism from other file or object
- ability to encrypt/decrypt values with ease
- expression on the config to have flexibility to the environments

One can argue, it is better to put into PY file, however, having config
in python script may give too much power than what it requires.

Install
~~~~~~~

.. code:: bash

   [sudo] pip install conff

Basic Usage
~~~~~~~~~~~

To get very basic parsing: #### parse object

.. code:: python

   import conff
   r = conff.parse({'math': '1 + 3'})
   r = {'math': '4'}

load YAML file
^^^^^^^^^^^^^^

.. code:: python

   import conff
   r = conff.load('path_of_file.yaml')

import files
^^^^^^^^^^^^

.. code:: python

   import conff
   ## y1.yml
   # shared_conf: 1
   ## y2.yml
   # conf: F.inc('y1.yml')

   r = conff.load('y2.yml')
   r = {'conf': {'shared_conf': 1}}

Examples
~~~~~~~~

More advances examples:

parse with simple expression
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   import conff
   r = conff.parse('1 + 2')
   r = 3

parse object
^^^^^^^^^^^^

.. code:: python

   import conff
   r = conff.parse({"math": "1 + 2"})
   r = {'math': 3}

ignore expression (declare it as string)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   import conff
   r = conff.parse('"1 + 2"')
   r = '1 + 2'

parse error behaviours
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   import conff
   errors = []
   r = conff.parse({"math": "1 / 0"}, errors=errors)
   r = {'math': '1 / 0'}
   errors = [['1 / 0', ZeroDivisionError('division by zero',)]]

parse with functions
^^^^^^^^^^^^^^^^^^^^

.. code:: python

   import conff
   def fn_add(a, b):
       return a + b
   r = conff.parse('F.add(1, 2)', fns={'add': fn_add})
   r = 3

parse with names
^^^^^^^^^^^^^^^^

.. code:: python

   import conff
   r = conff.parse('a + b', names={'a': 1, 'b': 2})
   r = 3

parse with extends
^^^^^^^^^^^^^^^^^^

.. code:: python

   import conff
   data = {
       't1': {'a': 'a'},
       't2': {
           'F.extend': 'R.t1',
           'b': 'b'
       }
   }
   r = conff.parse(data)
   r = {'t1': {'a': 'a'}, 't2': {'a': 'a', 'b': 'b'}}

parse with updates
^^^^^^^^^^^^^^^^^^

.. code:: python

   import conff
   data = {
       't1': {'a': 'a'},
       't2': {
           'b': 'b',
           'F.update': {
               'c': 'c'
           },
       }
   }
   r = conff.parse(data)
   r = {'t1': {'a': 'a'}, 't2': {'b': 'b', 'c': 'c'}}

parse with extends and updates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   import conff
   data = {
       't1': {'a': 'a'},
       't2': {
           'F.extend': 'R.t1',
           'b': 'b',
           'F.update': {
               'a': 'A',
               'c': 'c'
           },
       }
   }
   r = conff.parse(data)
   r = {'t1': {'a': 'a'}, 't2': {'a': 'A', 'b': 'b', 'c': 'c'}}

Test
~~~~

To test this project:

.. code:: bash

   nose2

TODO
~~~~

-  Add more coverage on python versions
-  More documentation on readthedocs

Other Open Source
~~~~~~~~~~~~~~~~~

This opensource project uses other awesome projects:
```Munch`` <https://github.com/Infinidat/munch>`__
```simpleeval`` <https://github.com/danthedeckie/simpleeval>`__
```cryptography`` <https://github.com/pyca/cryptography>`__