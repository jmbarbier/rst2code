Command line
============

Command line interface
----------------------

For vanilla reStructuredText (that can directly be parsed with docutils), we have to implement
a command line interface (main() function), using argparse ::

    #@@imports@@
    import argparse
    import sys

then we define our main function, to parse command line arguments and options, and to do the actual processing
of input files ::

    #@@command_line_actions@@
    class Usage(Exception):
        def __init__(self, msg):
            self.msg = msg

    def main(argv=None):
        global OUTPUT_DIR
        if argv is None:
            argv = sys.argv[1:]
        try:
            try:
                parser = argparse.ArgumentParser("Write code from rst files")
                parser.add_argument('outdir', metavar="OUTPUT_DIR", type=str, nargs=1,
                                    help="Output directory base for code")
                parser.add_argument('srcfiles', metavar="SRC_FILES", type=str, nargs=argparse.REMAINDER,
                                    help="Source files (.rst files)")
                parser.add_argument('--debug', '-d', action='store_true')
                args = parser.parse_args(argv)
            except Exception as msg:
                 raise Usage(msg)
    
    
            # process arguments
            DEBUG = args.debug
            if DEBUG:
                logging.basicConfig(level=logging.DEBUG)
            else:
                logging.basicConfig(level=logging.WARNING)
            OUTPUT_DIR = args.outdir[0]
            SRC_FILES = args.srcfiles
    
            for filename in SRC_FILES:
                scan_file(filename)
            process_blocks()
            clean_output_dir()
            write_files()
            return 0
    
        except Usage as err:
            print(sys.argv[0].split('/')[-1].split('\\')[-1] + ': ' \
                  + str(err.msg))
            print ("for help use --help")
            return 2
    
    if __name__ == "__main__":
        sys.exit(main())



RST files scan
--------------

We use docutils for rst files scan ::

    #@@imports@@
    from docutils.core import publish_doctree

We make docutils scan source rst files from command line, getting a doctree if no syntax error found, then we
check every item in doctree against literal_block type ::

    #@@input_file_analysis@@
    def scan_doctree(doctree, filename=""):
        for item in doctree.traverse():
            if item.tagname == "literal_block":
                get_block(item, filename)
    
    
    
    def scan_file(filename):
        with open(filename, "r") as f:
            lines = f.read()
        doctree = publish_doctree(lines)
        scan_doctree(doctree, filename)


Then each doctree literal_block item is analyzed to get its name (with getBlock).
