__author__ = 'jmbarbier'
#!python
# SEE: http://fr.slideshare.net/doughellmann/better-documentation-through-automation-creating-docutils-sphinx-extensions

from docutils.core import publish_doctree
import re
import sys
import getopt
import sys
import argparse
import logging
import os
import shutil

logging.basicConfig(level=logging.ERROR)

# GLOBALS
BLOCKS = {}
DEBUG = 0
OUTPUT_DIR = "./src"
fileblocks = {}
codeblocks = {}
MAX_ITERATIONS = 10

# REGULAR EXPRESSIONS
macro = r"@@([@\w/.+! -]+)@@"
macro_in_code = "^(\s*).*?@@([@\w/.+! -]+)@@.*$"


class CodeBlock(object):
    def __init__(self):
        self.name = ""
        self.is_file_block = False
        self.filename = ""
        self.content = ""
        self.language = ""
        self.iterations = 0
        self.replacement_done = False

    def macro_replace_step(self, blocks):
        logging.debug("Preparing blocks")
        logging.debug(self.content)
        if self.replacement_done:
            return True

        def macro_replace(match):
            indent = ""
            if match.group(1) is not None:
                indent = match.group(1)
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
                logging.warning("Unknown macro - not replaced")
                return match.group(0)

        if self.iterations > MAX_ITERATIONS:
            logging.warning("Replacemement max iterations done")
            return False
        self.iterations += 1
        self.content, n = re.subn(macro_in_code, macro_replace,
                                  self.content, flags=re.MULTILINE)
        if n==0:
            self.replacement_done = True
        return self.replacement_done



def store_block(block):
    """ Store block """
    logging.debug("Storing code block %s" % BLOCKS)
    if block.name not in BLOCKS.keys():
        BLOCKS[block.name] = []
    BLOCKS[block.name].append(block)


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


def scan_doctree(doctree, filename=""):
    for item in doctree.traverse():
        if item.tagname == "literal_block":
            get_block(item, filename)



def scan_file(filename):
    with open(filename, "r") as f:
        lines = f.read()
    doctree = publish_doctree(lines)
    scan_doctree(doctree, filename)

def clean_output_dir():
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def write_files():
    files = {}
    for blocks in BLOCKS.values():
        for block in blocks:
            if block.is_file_block:
                if block.name not in files.keys():
                    files[block.name] = []
                files[block.name].append(block.content)

    print("RST2CODE: Writing files : ",end="")
    for filename in files:
        destfile = os.path.abspath(os.path.join(OUTPUT_DIR + filename))
        d = os.path.dirname(destfile)
        if not os.path.exists(d):
            os.makedirs(d)
        with open(destfile, "w") as f:
            f.write("\n".join(files[filename]))
            print(".", end="")
    print("")


def process_blocks():
    logging.info("Generating code")
    running = True
    while running:
        for blocks in BLOCKS.values():
            for block in blocks:
                running = running and block.macro_replace_step(BLOCKS)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    try:
        try:
            parser = argparse.ArgumentParser("Write code from rst files")
            parser.add_argument('outdir', metavar="OUTPUT_DIR", type=str, nargs=1,
                                help="Output directory base for code")
            parser.add_argument('srcfiles', metavar="SRC_FILES", type=str, nargs="+",
                                help="Source files (.rst files)")
            parser.add_argument('--debug', '-d')
            args = parser.parse_args(argv)

        except Exception as msg:
             raise Usage(msg)


        # process arguments
        DEBUG = args.debug
        OUTPUT_DIR = args.outdir
        SRC_FILES = args.srcfiles

        for filename in SRC_FILES:
            scan_file(filename)
        process_blocks()
        return 0

    except Usage as err:
        print(sys.argv[0].split('/')[-1].split('\\')[-1] + ': ' \
              + str(err.msg) \
              , file=sys.stderr)
        print ("for help use --help", file=sys.stderr)
        return 2

def sphinx_get_doctree(app, doctree, docname):
    logging.debug("Got doctree")
    scan_doctree(doctree,docname)

def sphinx_build_finished(app, exception):
    env = app.builder.env
    OUTPUT_DIR = app.config.rst2code_output_dir
    process_blocks()
    clean_output_dir()
    write_files()

def setup(app):
    app.add_config_value("rst2code_output_dir", "./src", "env")
    app.add_config_value("rst2code_max_iterations", 10, "env")
    app.connect('doctree-resolved',sphinx_get_doctree)
    app.connect('build-finished', sphinx_build_finished)

if __name__ == "__main__":
    sys.exit(main())