from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="morngpt",
    version="1.0.0",
    author="mornGPT Team",
    author_email="team@morngpt.com",
    description="A comprehensive AI system with specialized modules for various use cases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuxuanzhouo3/mvp_26",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    keywords="ai, artificial intelligence, machine learning, specialized modules",
    project_urls={
        "Bug Reports": "https://github.com/yuxuanzhouo3/mvp_26/issues",
        "Source": "https://github.com/yuxuanzhouo3/mvp_26",
        "Documentation": "https://github.com/yuxuanzhouo3/mvp_26/blob/main/README.md",
    },
) 