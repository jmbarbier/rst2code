ReStructuredText parser
=======================

Le travail est déjà fait par docutils

.. code:: python
  :name: @@/parser.py@@

   from docutils.core import publish_doctree
   #@@imports@/parser.py@@

   #@@rest_text_parser@@

Il ne reste plus qu'à traverser le doctree et à processer les blocs de
texte littéral ::

  #@@rest_text_parser@@
  with open(sys.argv[1], "r") as f:
    lines = f.read()

  out = publish_doctree(lines)

  for item in out.traverse():
    if item.tagname == "literal_block":
      process_block(item)

Le process des blocks est fait dans le module process

.. code:: python
   :name: @@imports@/parser.py@@

   from process import process_block




TEST
====

Pour tester ::

  python test.py index.rst 
  from docutils.core import publish_doctree
  from process import process_block
  with open(sys.argv[1], "r") as f:
    lines = f.read()
  
  out = publish_doctree(lines)

  for item in out.traverse():
    if item.tagname == "literal_block":
      process_block(item)
  from docutils.core import publish_doctree
  from process import process_block
  with open(sys.argv[1], "r") as f:
    lines = f.read()
  
  out = publish_doctree(lines)
  
  for item in out.traverse():
    if item.tagname == "literal_block":
      process_block(item)
    {u'/parser.py': [{'content': u'from docutils.core import publish_doctree\n#@@imports@/parser.py@@\n\n#@@rest_text_parser@@', 'bname': u'/parser.py'}]}
