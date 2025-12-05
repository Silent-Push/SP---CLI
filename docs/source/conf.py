import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "SP - CLI"
copyright = "2024, Silent Push"
author = "Jorgeley<jorgeley@silentpush.com>"
version = release = "1.3.0"
show_authors = True

extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
]
highlight_language = "python"
pygments_style = "sphinx"
autosummary_generate = True  # Turn on sphinx.ext.autosummary
autosummary_show_inherited_class_members = True
autodoc_default_options = {
    "class-doc-from": "class",
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
    # "inherited-members": "BaseCommandSet, BaseCommand, padns, spql",
    "show-inheritance": True,
    "private-members": True,
    "special-members": "__enter__, __exit__",
    "exclude-members": "_",
    "no-value": True,
}
autodoc_typehints = "both"
autodoc_class_signature = "separated"
exclude_patterns = ["build", "docs", "_autosummary"]

html_theme = "classic"
html_logo = "../logo.svg"
html_favicon = "../favicon.ico"
html_title = "Silent Push - CLI"
html_use_index = False
html_domain_indices = False
html_theme_options = {
    "stickysidebar": True,
    "sidebarwidth": "25%",
    # "relbarbgcolor": "#1c3138",
    # "bgcolor": "rgb(22, 38, 43)",
    # "textcolor": "white"
}
html_static_path = ["_static"]
