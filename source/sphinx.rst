Sphinx extension
================

   
Source file processing can be done with sphinx, we just need to respond to "doctree-resolved" event that
gives us processed doctree ::

    #@@sphinx_extension@@
    def sphinx_get_doctree(app, doctree, docname):

        if app.config.rst2code_debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.WARNING)

        logging.debug("Got doctree")
        scan_doctree(doctree,docname)

We wait for "build-finished" event to create source code files (SEE? maybe we should do it before ?) ::

    #@@sphinx_extension@@
    def sphinx_build_finished(app, exception):
        global OUTPUT_DIR
        env = app.builder.env
        OUTPUT_DIR = app.config.rst2code_output_dir
        process_blocks()
        clean_output_dir()
        write_files()


To use rst2code within sphinx, [configuration]... So we need a "setup" function ::

    #@@sphinx_extension@@
    def setup(app):
        app.add_config_value("rst2code_output_dir", "./src", "env")
        app.add_config_value("rst2code_max_iterations", 10, "env")
        app.add_config_value("rst2code_debug", False, "env")
        app.connect('doctree-resolved',sphinx_get_doctree)
        app.connect('build-finished', sphinx_build_finished)
 
