import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="worden-jvlsg",
    version="1.0.0",
    author="João Guimarães",
    author_email="fp17fb74lev8@opayq.com",
    description="TUI Space operations center",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jvlsg/Worden",
    packages=setuptools.find_packages(),
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