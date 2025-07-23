from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="morngpt",
    version="1.0.0",
    author="Yuxuan Zhou",
    author_email="yuxuan.zhou@example.com",
    description="Multi-Module AI System with Free AI Client Integration",
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
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "web": [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "pydantic>=2.5.0",
        ],
        "ai": [
            "google-generativeai>=0.3.0",
            "anthropic>=0.7.0",
            "huggingface-hub>=0.19.0",
            "openai>=1.3.0",
            "mistralai>=0.0.10",
            "cohere>=4.37",
        ],
    },
    entry_points={
        "console_scripts": [
            "morngpt=morngpt.cli:main",
            "morngpt-server=backend.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "morngpt": ["*.json", "*.yaml", "*.yml"],
    },
    keywords="ai, machine learning, prompt engineering, orchestration, free ai",
    project_urls={
        "Bug Reports": "https://github.com/yuxuanzhouo3/mvp_26/issues",
        "Source": "https://github.com/yuxuanzhouo3/mvp_26",
        "Documentation": "https://github.com/yuxuanzhouo3/mvp_26/docs",
    },
) 