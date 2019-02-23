import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edgar3",
    version="1.0",
    author="Ken Farr",
    author_email="ken@farr.ai",
    description="Yet another SEC Edgar Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kfarr3/edgar3',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
