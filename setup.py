from setuptools import setup, find_packages

setup(
    name="svg2tsv",
    version="1.1.1",
    description="A command-line tool to extract points from SVG paths and save them as a TSV matrix.",
    author="Brendan Harris",
    author_email="brendanjohnharris@gmail.com",
    url="https://github.com/brendanjohnharris/svg2tsv",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "svgpathtools",
        "numpy",
        "svgwrite",
    ],
    entry_points={
        "console_scripts": [
            "svg2tsv=svg2tsv.svg2tsv:main",
            "tsv2svg=svg2tsv.tsv2svg:main",
        ],
    },
)