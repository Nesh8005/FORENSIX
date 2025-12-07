from setuptools import setup, find_packages

setup(
    name="forensix-sentinel",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.0",
        "rich>=13.7.0",
        "colorama>=0.4.6",
        "tqdm>=4.66.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "PyYAML>=6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "forensix=forensix.cli:cli",
        ],
    },
)
