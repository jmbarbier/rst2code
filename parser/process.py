import re

from store import store_block

macro = re.compile("@@([@\w/.+! -]+)@@")
incodemacro = re.compile("^(\s)*.*@@([@\w/.+! -]+)@@.*")


def process_block(item):

    block = {}

    for name in item.attributes['names']:
        m1 = macro.match(name)
        if m1 is not None:
            # Got macro name from name attribute
            block['bname'] = m1.group(1)
            block['content'] = item.astext()
            break
    if block == {}:
        # Have to search in code : search in 1st line
        m2 = incodemacro.match(item.astext())
        if m2 is not None:
            block['bname'] = m2.group(2)
            block['content'] = "\n".join(item.astext().split("\n")[1:])
    if block == {}:
        print "UNKNOWN BLOCK, PASSED"
    else:
        store_block(block)
        
            
            
