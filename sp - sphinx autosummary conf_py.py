# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
sys.path.insert(0, os.path.abspath("../.."))

project = 'SP - SDK'
copyright = '2024, Silent Push'
author = 'Jorgeley<jorgeley@silentpush.com>'
version = release = '0.0.1'
show_authors = True

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]

autosummary_generate = True  # Turn on sphinx.ext.autosummary
autosummary_show_inherited_class_members = False
highlight_language = "python"
# toc_object_entries = False  # table of contents
# toc_object_entries_show_parents = "domain"

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "both"
autoclass_content = "class"  # Add __init__ doc (ie. params) to class summaries
autodoc_inherit_docstrings = False  # Do not inherit docstring from base class
autodoc_default_options = {
    "class-doc-from": "class",
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
    "inherited-members": "CommandSet, Cmd",
    "show-inheritance": False,
    "private-members": True,
    "special-members": "__enter__, __exit__",
    "exclude-members": "_",
}
# Don't show class signature with the class' name.
autodoc_class_signature = "separated"

templates_path = ['_templates']
exclude_patterns = ["build", "docs", "_autosummary"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'classic'
html_title = "Silent Push - SDK"
html_use_index = False
html_domain_indices = False
html_theme_options = {
    "stickysidebar": True,
    "sidebarwidth": "25%",
    # "relbarbgcolor": "rgb(33, 51, 56);",
    # "bgcolor": "rgb(22, 38, 43);"
}
html_static_path = ['_static']

