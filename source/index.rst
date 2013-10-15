rst2code source
===============

Written with rst2code :)

Program structure
------------------

**rst2code** program structure is the following ::

  #@@/rst2code.py@@
  #@@python_headers@@
  #@@license@@

  #@@imports@@

  #@@globals@@
  #@@regular_expressions@@

  #@@objects@@

  #@@blocks_storage@@
  #@@block_processing@@
  #@@block_analysis@@

  #@@file_operations@@
  #@@files_generator@@
  
  #@@input_file_analysis@@
  
  #@@command_line_actions@@
  
  #@@sphinx_extension@@

Logging can be enabled for debug / trace purposes ::

    #@@imports@@
    import logging

Code blocks
-----------

Structure
~~~~~~~~~

A block is a named portion of code ::

  #@@objects@@
  class CodeBlock(object):
      def __init__(self):
          self.name = ""
          self.is_file_block = False
          self.filename = ""
          self.content = ""
          self.language = ""
          self.iterations = 0
          self.replacement_done = False
      
      
      #@@codeblock_actions@@

Fields are :

- name : code block name (many code blocks can have the same name, in this case their content is appended).

- is_file_block : True if block is outputted directly into af file

- filename : source (.rst file) filename for this block (not used for now).

- content : source content

- language : source language (if defined, not used for now)

- iterations : when a code block is processed to replace macros, inserted code can introduce new macros. rst2code makes
  MAX_ITERATIONS maximum of macro replacing ::
  
      #@@globals@@
      MAX_ITERATIONS = 10

- replacement_done : macro replacement is over

Block from doctree
~~~~~~~~~~~~~~~~~~

With docutils rst file parsing, we obtain a doctree; for every "literal_block" item (code, code-block, ...),
we have to search an identifier (in :name: option or in code first line) ::

    #@@block_analysis@@
    def get_block(item, filename):
        """
        Get block from doctree item
        """
        logging.info("Getting code block")
        block = CodeBlock()
        block.filename = filename
        for name in item.attributes['names']:
            m1 = re.match(macro, name)
            if m1 is not None:
                # Got macro name from name attribute
                block.name = m1.group(1)
                block.content = item.astext()
                block.is_file_block = block.name[0]=="/"
                break
        if block.name == "":
            # Have to search in code : search in 1st line
            m2 = re.match(macro_in_code, item.astext(), re.MULTILINE)
            if m2 is not None:
                block.name = m2.group(2)
                block.content = "\n".join(item.astext().split("\n")[1:])
                block.is_file_block = block.name[0]=="/"
        if block.name == "":
            logging.info("Block is not macro block")
            return False
        else:
            logging.debug("Have code block")
            store_block(block)
            return True




Storage
~~~~~~~

Blocks are stored into a global dictionary named BLOCKS ::

  #@@globals@@
  BLOCKS = {}

Each block is stored in an array ::

    #@@blocks_storage@@
    def store_block(block):
        """ Store block """
        logging.debug("Storing code block %s" % BLOCKS)
        if block.name not in BLOCKS.keys():
            BLOCKS[block.name] = []
        BLOCKS[block.name].append(block)


Transformation
~~~~~~~~~~~~~~

Regular expressions are used to search macro name in code blocks ::

    #@@regular_expressions@@
    macro = r"@@([@\w/.+! -]+)@@"
    macro_in_code = "^([ ]*).*?@@([@\w/.+! -]+)@@.*$"

(so we have to import re) ::

    #@@imports@@
    import re
    
Code blocks content is searched for macro names, and each found macro is replaced by its content. If no macro is
found with this name, comment block is left untouched.

If no macro name is found inside code, or if iterations are more than MAX_ITERATIONS,
then macro transformation returns False  ::

    #@@codeblock_actions@@
    def macro_replace_step(self, blocks):
        logging.debug("Preparing blocks")
        logging.debug(self.content)
        if self.replacement_done:
            return 0

        def macro_replace(match):
            indent = ""
            if match.group(1) is not None:
                indent = match.group(1)
                if len(indent)>0 and indent[0]=="\n":
                    if len(indent)>1:
                        indent=indent[1:]
                    else:
                        indent=""
                logging.debug("INDENT:|%s|" % indent)
            logging.debug("Replacing %s", match.group(2))
            if match.group(2) in BLOCKS.keys():
                # Found a macro : replace with it
                out = ""
                for b in BLOCKS[match.group(2)]:
                    for line in b.content.split("\n"):
                        out += indent+line+"\n"
                logging.debug("OUT %s" % out)
                return out
            else:
                # Macro not found, don't replace anything
                logging.warning("@@%s@@ : unknown macro - not replaced" % match.group(2))
                return match.group(0)

        if self.iterations > MAX_ITERATIONS:
            logging.warning("Replacemement max iterations done")
            return 0
        self.iterations += 1
        self.content, n = re.subn(macro_in_code, macro_replace,
                                  self.content, flags=re.MULTILINE)
        if n==0:
            self.replacement_done = True
        return n



All blocks are transformed looping with this macro_replace_step above ::

    #@@block_processing@@
    def process_blocks():
        logging.info("Generating code")
        replaced = 1
        while replaced != 0:
            replaced = 0
            for blocks in BLOCKS.values():
                for block in blocks:
                    result = block.macro_replace_step(BLOCKS)
                    replaced += result

Files output
------------

Output directory is defined as OUTPUT_DIR global ::

    #@@globals@@
    OUTPUT_DIR = "./src"
    
using shutil.rmtree and os.walk ::

    #@@imports@@
    import shutil, os

it can be cleaned ::

    #@@file_operations@@
    def clean_output_dir():
        for root, dirs, files in os.walk(OUTPUT_DIR):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))


All blocks are scanned, file block contents are concatened then written to file ::

    #@@files_generator@@
    def write_files():
        files = {}
        for blocks in BLOCKS.values():
            for block in blocks:
                if block.is_file_block:
                    if block.name not in files.keys():
                        files[block.name] = []
                    files[block.name].append(block.content)
    
        print("RST2CODE: Writing files : ")
        for filename in files:
            destfile = os.path.abspath(os.path.join(OUTPUT_DIR + filename))
            d = os.path.dirname(destfile)
            if not os.path.exists(d):
                os.makedirs(d)
            with open(destfile, "w") as f:
                f.write("\n".join(files[filename]))
                print(filename)
        print("")

