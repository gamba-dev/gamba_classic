Development
=============

.. contents:: Table of contents:
   :local:

Contributing to gamba
----------------------
Thank you for your interest in gamba's development - this page should help with understanding the development process, and how best to apply your skills! If at any point you have questions that you can't find answers to, please email `dev@gamba.dev <mailto:dev@gamba.dev>`_


Where to start?
+++++++++++++++++++++++++
The best place to find where help is needed is the `github issues page <https://github.com/gamba-dev/gamba/issues>`_, especially those tagged with the 'good first issue' label. These can be loosely grouped into feature requests, bug fixes, and documentation improvements - see the below sections for details;


Adding Features
+++++++++++++++++++++++++
To add a feature to the gamba library, such as a new analytical or data cleaning method, you will first need to :ref:`install gamba as a developer<dev install>`. From there, `create a new local branch <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-branches>`_ and start work adding your feature.

As gamba is in the early stages of development, there are currently no fixed rules to adding new features, although common sense applies. Please read through other methods to get the rough coding style, how to document your new method, and to understand where in the library it makes sense to add your new feature!

Once you're happy that your new feature works as intended, and you've tested it and have examples of it working, `create a pull request <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests>`_. Again, there are currently no fixed rules on formatting this request, although we're currently experimenting with `pull request templates <https://help.github.com/en/github/building-a-strong-community/creating-a-pull-request-template-for-your-repository#adding-a-pull-request-template>`_. As a minimum please be sure to include a `reference to the issue <https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax#referencing-issues-and-pull-requests>`_ your pull request addresses, and a description of the changes/additions it makes.

If everything looks good and works as intended, your pull request will be merged to the main branch by one of the core developers (`ojscholten <https://github.com/ojscholten>`_)!


Fixing Bugs
+++++++++++++++++++++++++
Bug fixes are always welcome and follow the same workflow as adding features above. In your pull request fixing a bug, please reference the issue and provide a quick description of how you fixed it!

As with new features, if everything looks good and your fix addresses an existing issue, your pull request will be merged. Also, if you come across a bug which isn't already on the `issues page <https://github.com/gamba-dev/gamba/issues>`_, please create an issue for it so that it's clear what the pull request is for!


Improving Documentation
+++++++++++++++++++++++++
Improving documentation doesn't have to have as many steps as the contributions above. Please feel free to open any of the files in the repository through the `github repo website <https://github.com/gamba-dev/gamba>`_ and change the files directly using the built-in file editor (pencil icon in the top right of each file).

Once you've made an edit, please provide a quick description of it if it's not immediately obvious what the change is, and it will be merged!


Communication
-----------------
If you're looking to contribute to gamba in any of the above ways and encounter difficulties, please email `dev@gamba.dev <mailto:dev@gamba.dev>`_ and we'll be happy to help! Please also remember that this project has been developed as an open-source, open-science project, as such, any issues surrounding the methods used in papers for example, should be directed to the authors of those papers as opposed to the gamba development team!

Please note that gamba's development and communications follow `the Contributor Covenant's code of conduct <https://www.contributor-covenant.org/version/1/3/0/code-of-conduct/>`_ - the contact email for any such issues is `oliver@gamba.dev <mailto:oliver@gamba.dev>`_.



Project Roadmap
-----------------

gamba's development aims to improve the library in three key areas;

1. coverage of player behaviour tracking studies
2. computational efficiency on large datasets
3. ease of use, particularly for Python beginners

Each of these aims, whilst broad, brings a collection of tasks which are currently unfininshed. For a list of currently open issues, see the `repository issues page <https://github.com/gamba-dev/gamba/issues>`_. Each issue is not explicitly labelled with respect to the areas above, but they should be kept in mind when contributing code, documentation, and other resources.

There is currently no strict time-frame for gamba's development roadmap - as such, if you feel you can contribute to any of these areas, or indeed anything surrounding this project, please get in touch and get involved!











