"""Setup configuration for code_tokenizer."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code_tokenizer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for tokenizing and analyzing code files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code_tokenizer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.12",
    install_requires=[
        "tiktoken>=0.9.0",
        "pygments>=2.17.2",
        "rich>=13.7.0",
        "pathspec>=0.12.1",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "code-tokenizer=code_tokenizer.__main__:main",
        ],
    },
)
