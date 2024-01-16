import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-solarfrontier",
    version="0.1.0",
    author="ernestasga",
    description="Library to communicate with Solar Frotier inverters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ernestasga/python-solarfrontier",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
