from docutils.core import publish_doctree
import sys

# GLOBALS

BLOCKS = {}

# Process block
def process_block(item):
    






for filename in sys.argv[2:]:
    with open(filename, "r") as f:
        lines = f.read()
    doctree = publish_doctree(lines)
    for item in out.traverse():
        if item.tagname == "literal_block":
            process_block(item)

generate_code()

# GLOBALS


if is_codeblock(item):
    b = codeBlock()
    b.getFromDocTreeItem(item)

# CLASSES

class codeBlock:
    name=""
    src=""
    btype=""
    content=""
    language=""

    @static
    def isCodeBlock(item)

class Blocks:
    blocks= {}

    def addBlock(self, block):
        if not self.blocks.has_key(block.name):
            self.blocks[block.name] = []
        self.blocks[block.name] = block
