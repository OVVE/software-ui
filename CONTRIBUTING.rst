==========================
Contributing to OVVE
==========================

OVVE is primarily developed by `https://lifemech.org/`_, but we welcome contributions.

Code Contributions
------------------
OVVE tracks many issues internally, but we use github's `issue tracker`_
for public facing issues.  Feel free to browse the issues there and tackle
any you feel equipped to do.  When you update or add comments to an issue. 

You should ensure the following are true for any PR before it will be 
considered for review or re-review

- The code and architecture comply with `Standards and Best Practices`_
- Any UI components comply with the project `Style Guide`_
- Contributions follow any subsystem specific practices (example: `Javascript Guide`_)
- Automated regression and integration tests are passing
- Any automated feedback (label bot, lint bot, etc) is addressed
- Any previous developer feedback is addressed

Before submitting a PR, review our `Guide to Authoring Pull Requests`_.  
if you have questions or need feedback do write to xyz@lifemech.org


Bug Reports
-----------
To file a bug report, please follow the system outlined in our `bug
reports`_ wiki page.  You are also welcome to submit an accompanying pull
request if you are able to resolve the issue.

Documentation Contributions
---------------------------
Technical documentation is available at `Read the Docs`_.
It is written in reStructuredText_.

The User Configurable Reporting documentation also shows another good
practice; it uses reStructuredText's autoclass_ directive to include the
documentation written as docstrings in the codebase. This avoids
duplication, and means that when the codebase is changed, the documentation
is updated automatically with it.

Add a file to the *docs/* directory, and a reference to it in
*docs/index.rst* under the ``toctree`` directive, to include it with the
rest of OVVE documentation. 


.. _Lifemech: http://www.lifemech.org/
.. _issue tracker: https://github.com/OVVE/software-ui/issues/
.. _Standards and Best Practices: https://github.com/OVVE/STANDARDS.rst
.. _Guide to Authoring Pull Requests: https://github.com/OVVE/open-source/docs/Writing_PRs.md
.. _Read the Docs: https://OVVE.readthedocs.io/
.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _autoclass: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html


Updating requirements
---------------------
To update requirements edit:

* ``requirements.txt`` for packages for all environments



QA / Work in progress
~~~~~~~~~~~~~~~~~~~~~~
PRs that are not ready to be merged can be labeled with one of the following labels:

- awaiting QA
- Open for review: do not merge

As long as either of these labels are present on the PR it will have a pending status.