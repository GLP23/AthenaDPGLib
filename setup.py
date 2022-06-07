# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import setuptools

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
setuptools.setup(
    name="AthenaGuiLib",
    version="0.2.0",
    author="Andreas Sas",
    author_email="",
    description="A Library of DearPyGui elements, to be used in Directive Athena projects",
    url="https://github.com/DirectiveAthena/AthenaGuiLib",
    project_urls={
        "Bug Tracker": "https://github.com/DirectiveAthena/AthenaGuiLib/issues",
    },
    license="GPLv3",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "DearPyGui>=1.6.2",
        "AthenaLib>=0.2.0",
        "AthenaColor>=5.1.0"
    ]
)