import setuptools
import worden.const
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="worden",
    version=worden.const.VERSION,
    author="João Guimarães",
    author_email="jvlsg-github@ipriva.org",
    description="TUI Space operations center",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jvlsg/Worden",
    entry_points={'console_scripts': ['worden=worden.__main__:run_app'], },
    packages=setuptools.find_packages() 
    + ["worden.src","worden.src.api","worden.src.ui"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console :: Curses",
        "Intended Audience :: Education",
        "Natural Language :: English"
    ],
    python_requires='>=3.7',
    install_requires=[
        "Pillow>=5.4.1",
        "drawille>=0.1.0",
        "npyscreen>=4.10.5"],    
)