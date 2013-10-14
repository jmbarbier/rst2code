Welcome to rst2code's documentation!
====================================


**rst2code** is a literate programming tool.

The goal
--------

The goal is to be able to write code at the same time that documentation. More precisely, **rst2code** allows to
generate code from documentation, whereas many tools - pycco, docco, doxygen, sphinx, are designed to extract
documentation from code.

As human reading and understanding order is not the same than computer's, **rst2code** allows us to write code
in any order, reassembling code blocks at "compile" time to obtain real source code suitable for computer use.

**rst2code** is code agnostic (normally.. i tried it with python, html and coffee-script for now)

For the sake of readability, code blocks included in documentation should be easily syntax highligted (this means that
a code block should be more or less valid code)


Syntax
------


Code blocks are written in ... well, reStructuredText code blocks directives ( code / code-block / sourcecode / :: )

Each code block is named, using code block name options (if available), or within a comment in the first line of
code block. Names are in @@MACRONAME@@ form (characters surrounded by two @) :



.. code-block:: rest

  .. code-block:: langage

     #@@MACRONAME@@ (within language comment)
     Code

or

.. code-block:: rest

  .. code:: language
    :name: @@MACRONAME@@

    Code

or

.. code-block:: rest

  ::

    @@MACRONAME@@ (within language comment)


If **name** option is available, it is used to get block comment name.

If not, or if no block name is found in **name** option, the first line of source code should
contain the name inside a comment (language dependant), using the format @@MACRONAME@@.

If no block name is found, the block is not used in **rst2code**


MACRONAMES definitions are :

* */STARTING/WITH/SLASH* : file generation definitions. The file is
  created the first time macro definition is seen with path appended
  to source code output directory. If other definitions are seen
  after, code is simply appended.

* *NOT/STARTING/WITH/SLASH* : program text definitions. If many
  definitions are seen with same name, behaviour is undefined for the
  moment.


Inside the code blocks, **rst2code** detect comments containing @@MACRONAMES@@
strings, remove the comment while retaining indentation for every line
in macro content and then replace it.

Usage
-----

With "standard" reStructuredText ::

  $ rst2code [OPTIONS] DEST_DIR RST_FILE1 RST_FILE2 RST_FILE3 ...


With "sphinx-flavoured" .rst files : just add "rst2code" to sphinx extensions, and
set rst2code_output_dir config option and launch any sphinx document generation.

**Current rst2code module have been written from this documentation**


Contents:

.. toctree::
   :maxdepth: 2

   source/index
   source/cmdline
   source/sphinx
   source/misc

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

