from setuptools import setup, find_packages


setup(
    name="quantlib",
    version="0.1.0",
    description="quantlib - a quantitative finance library and cli",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "pandas>=2.3.3",
        "numpy>=2.4.0",
    ],
    entry_points={
        "console_scripts": [
            "quantlib=cli.main:main",
        ]
    },
)
