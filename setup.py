from setuptools import setup, find_packages

setup(
    name="botwell",
    version="1.2.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "numpy",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "botwell=botwell.cli:main",
        ],
    },
    author="Referential",
    author_email="info@referential.ai",
    description="Boswell Test - LLM Comparative Analysis Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/referential-ai/boswell-test",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)