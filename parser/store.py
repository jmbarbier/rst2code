fileblocks = {}
codeblocks = {}

def store_block(block):
    b = block['bname']
    if b[0]=="/":
        dest = fileblocks
    else:
        dest = codeblocks
    if not dest.has_key(b):
        dest[b] = []
    dest[b].append(block)


