import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

PROJECT_URLS = {
	"Documentation": "https://gamba.dev",
    "Source Code": "https://github.com/gamba-dev/gamba",
    "Twitter": "https://twitter.com/gamba_dev"
}
CLASSIFIERS = [
    	"Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering"
]

setuptools.setup(
    name="gamba",
    version="0.1.0",
    author="Oliver J. Scholten",
    author_email="oliver@gamba.dev",
    description="gambling transaction analysis in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gamba-dev/gamba",
    packages=setuptools.find_packages(),
    project_urls=PROJECT_URLS,
    classifiers=CLASSIFIERS,
    python_requires='>=3.8',
    zip_safe=False,

    install_requires=[
        "pandas >= 1.0.3",
        "matplotlib >= 3.2.1",
        "scikit-learn >= 0.23.0",
        "statsmodels >= 0.11.1",
        "tqdm >= 4.48.2",
    ],

    extras_require = {
        "dev" : [
            "pytest >= 3.7",
      ],

    },
)


import matplotlib.pyplot as plt
import matplotlib as mpl

import os
import shutil

gb_style_file = os.getcwd() + '/gamba/gamba.mplstyle'
mpl_style_dir = mpl.get_data_path() + '/stylelib'

print('copying gamba style into matplotlib style library...')
shutil.copy(gb_style_file, mpl_style_dir)
print('gamba plot style installed.')



# ====================================================
# note to self: 

# first, remove the old dist/
# rm -R dist/

# then, create the new one (check version number!!!!!)
# python3 setup.py sdist bdist_wheel

# finally, upload it to PyPI using twine
# python3 -m twine upload dist/*

# ====================================================