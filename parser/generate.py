import re
import store

macro = "(\s)*.*@@([@\w/.+! -]+)@@.*"

def macrorepl(m):
    cb = store.codeblocks
    if cb.has_key(m.group(2)):
        newc =  [b['content'] for b in cb[m.group(2)]]
        return m.group(1)+"\n".join(newc)
    else:
        return m.group(1)


def generate_code(fb,cb):
    for codes in fb.values():
        for block in codes:
            code = block['content']
            while True:
                code, n = re.subn(macro, macrorepl, code, re.M)
                print code
                if n == 0:
                    break
        
    print fb
