from docutils.core import publish_doctree
from process import process_block
from generate import generate_code
import store
import sys

with open(sys.argv[1], "r") as f:
    lines = f.read()

out = publish_doctree(lines)

for item in out.traverse():
    if item.tagname == "literal_block":
        process_block(item)

generate_code(store.fileblocks,store.codeblocks)
