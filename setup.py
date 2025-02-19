"""Setup configuration for code_tokenizer."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Core dependencies required for the package to function
INSTALL_REQUIRES = [
    "tiktoken>=0.9.0",
    "pygments>=2.17.2",
    "rich>=13.7.0",
    "pathspec>=0.12.1",
    "python-dotenv>=1.0.0",
    "setuptools>=69.0.0",
    "setuptools_scm>=8.0.0",
    "wheel>=0.42.0",
]

# Development dependencies for testing, linting, etc.
DEV_REQUIRES = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "pytest-benchmark>=4.0.0",
    "black>=24.2.0",
    "isort>=5.13.2",
    "flake8>=7.0.0",
    "mypy>=1.8.0",
    "coverage>=7.4.1",
    "build>=1.0.3",
    "twine>=4.0.2",
    "types-setuptools>=69.0.0.0",
    "types-pygments>=2.17.0.0",
    "types-python-dotenv>=1.0.0.0",
]

setup(
    name="code_tokenizer",
    version="0.0.1",
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
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": DEV_REQUIRES,
    },
    entry_points={
        "console_scripts": [
            "code-tokenizer=code_tokenizer.__main__:main",
        ],
    },
)
