# rst2code : reStructuredText literal programming tool

rst2code is a literal programming tool. See [index.rst](documentation) for more details

WARNING: this is a python3-only program for now.

## Testing with sphinx

### Building with itself, hacking around

    git clone https://github.com/jmbarbier/rst2code.git
    cd rst2code
    virtualenv --python=python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
    make html

Then a src/rst2code.py file should appear.

### Using it

    pip install git+git://github.com/jmbarbier/rst2code.git@master
    # Create a sphinx documentation
    sphinx-quickstart
    # Edit conf.py, add 'rst2code' to extensions
    # Edit index.rst, add for example 
    Testing ::

	#@@/test.py@@
        print("Hello, world")

    # Launch sphinx
    make html
    # A directory src containing test.py should appear.  
