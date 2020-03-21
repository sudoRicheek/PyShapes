import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyShapes", # Replace with your own username
    version="1.1.1",
    author="Richeek Das",
    author_email="richeekdas2001@gmail.com",
    description="A shape detection module for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sudoRicheek/PyShapes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)