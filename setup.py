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
def version_handler() -> str:
    version = 1,0,0
    return ".".join(str(i) for i in version)

setuptools.setup(
    name="AthenaDearPyGuiLib",
    version=version_handler(),
    author="Andreas Sas",
    author_email="",
    description="A Library of DearPyGui elements, to be used in Directive Athena projects",
    url="https://github.com/DirectiveAthena/AthenaDearPyGuiLib",
    project_urls={
        "Bug Tracker": "https://github.com/DirectiveAthena/AthenaDearPyGuiLib/issues",
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
