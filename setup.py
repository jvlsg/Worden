import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="worden",
    version="1.0.0",
    author="João Guimarães",
    author_email="jvlsg-github@ipriva.org",
    description="TUI Space operations center",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jvlsg/Worden",
    #packages=setuptools.find_packages(where="worden_pkg", include=["src.*",]),
    packages=["worden_pkg","worden_pkg.src.api","worden_pkg.src.ui"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console :: Curses",
        "Intended Audience :: Education",
        "Natural Language :: English"
    ],
    python_requires='>=3.7',
)