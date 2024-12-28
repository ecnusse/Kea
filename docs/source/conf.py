import os
import sys

sys.path.insert(0, os.path.abspath("../../"))
# sys.path.insert(0, os.path.abspath("../kea"))
# Configuration file for the Sphinx documentation builder.

# -- Project information

project = "Kea"
copyright = (
    "2024, Yiheng Xiong, Ting Su, Jue Wang, Jingling Sun, Geguang Pu, Zhendong Su"
)
author = "Yiheng Xiong, Ting Su, Jue Wang, Jingling Sun, Geguang Pu, Zhendong Su"

release = "1.0.1"
version = "1.0"


# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"

pygments_style = "sphinx"

latex_engine = "xelatex"
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "preamble": r"""
\usepackage{xeCJK}
\setCJKmainfont[BoldFont=STZhongsong, ItalicFont=STKaiti]{STSong}
\setCJKsansfont[BoldFont=STHeiti]{STXihei}
\setCJKmonofont{STFangsong}
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt
\parindent 2em
\definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
\setcounter{tocdepth}{3}
\renewcommand\familydefault{\ttdefault}
\renewcommand\CJKfamilydefault{\CJKrmdefault}
""",
}
