.. rstlit documentation master file, created by
   sphinx-quickstart on Sat Oct 12 23:22:07 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to rstlit's documentation!
==================================

**rstlit** est un outil de programmation littérale que je vais essayer
de créer pour répondre à un besoin que j'ai depuis des années et que
je n'ai pas pu combler en utilisant les outils existants.

Le principe
-----------

Le principe est d'écrire le code en même temps que la documentation,
et plus précisément de pouvoir générer le code à partir de la
documentation. Contrairement aux outils permettant de générer la
documentation à partir du code (docco, doxygen), ici l'idée est de
générer le code à partir de la documentation.

L'ordre de lecture et de compréhension d'un humain n'étant pas
forcément celui d'un ordinateur, la documentation doit pouvoir
présenter les morceaux de codes dans un ordre différent de celui du
code pour l'ordinateur.

La documentation doit pouvoir être utilisable directement, sans avoir
à être transformée. Le code, en revanche, est généré par lecture de la
documentation.

L'outil doit être multi-languages.

Les morceaux de code générés doivent pouvoir être valide avec un
"surligneur de syntaxe" directement.

Proposition de syntaxe

.. code-block:: rest

  .. code-block:: langage

     #MACRONAME definition
     Code with #@@MACRONAME2@@ in comments

If the first line of source code is a comment (language dependant)
containing the special (unescaped) syntax @@MACRONAME@@, the code
block have to be considered by the program generator.

MACRONAMES definitions are :

* */STARTING/WITH/SLASH* : file generation definitions. The file is
  created the first time macro definition is seen with path appended
  to source code output directory. If other definitions are seen
  after, code is simply appended.

* *NOT/STARTING/WITH/SLASH* : program text definitions. If many
  definitions are seen with same name, behaviour is undefined for the
  moment.


Inside the program lines, we detect comments containing @@MACRONAMES@@
strings, remove the comment while retaining indentation for every line
in macro content and then replace it. Circular references have to be
detected.

L'invocation du code est faite par la ligne de commande suivante ::

  $ rst2code [OPTIONS] DEST_DIR RST_FILE1 RST_FILE2 RST_FILE3 ...

Le programme se compose donc de la manière suivante ::

  #@@/rst2code.py@@

  #@@python headers@@
  #@@license@@
  #@@imports@@
  #@@command line arguments@@
  #@@rst file parser@@
  #@@blocks analysis@@
  #@@code generator@@



Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

