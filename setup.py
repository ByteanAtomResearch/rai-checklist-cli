from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rai-checklist-cli",
    version="0.6.0",
    author="Noble Ackerson",
    author_email="noblel@byteanatom.com",
    description="A CLI tool to generate responsible AI checklists for machine learning projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ByteanAtomResearch/rai-checklist-cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'rai-checklist=rai_checklist_cli.cli:main',
        ],
    },
    install_requires=[
        'pyyaml',
        'tqdm',
    ],
    include_package_data=True,
    package_data={
        'rai_checklist_cli': ['templates.yaml'],
    },
)