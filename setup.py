from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="geotify",
    version="1.0.0",
    author="Yeogyeong, Song",
    author_email="challengef0802@gmail.com",
    description="Visualization tools suitable for geographic data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "geotify": "https://github.com/Geotifying/geotify.git",
    },
    classifiers=[
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
)
