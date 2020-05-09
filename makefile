# Minimal makefile for Sphinx documentation

SPHINXBUILD   = sphinx-build
SPHINXPROJ    = gamba
SOURCEDIR     = docs/
BUILDDIR      = build


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

clean:
	rm -R build/
	#find . -name .ipynb_checkpoints -type d -print0|xargs -0 rm -r --
	#sudo python setup.py install
	
%: makefile

	pip install --upgrade --force-reinstall ../gamba

	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)