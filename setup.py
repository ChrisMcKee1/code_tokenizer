from setuptools import find_packages, setup

setup(
    name="code-tokenizer",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "tiktoken",  # For token counting
        "pygments",  # For language detection and syntax highlighting
        "rich",  # For beautiful terminal output
        "pathspec",  # For gitignore pattern matching
    ],
    entry_points={
        "console_scripts": [
            "code-tokenizer=code_tokenizer.cli:main",
        ],
    },
    author="Chris McKee",
    author_email="your.email@example.com",
    description="Transform your codebase into LLM-ready tokens with intelligent processing",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chrismckee/code-tokenizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
