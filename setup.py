import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eegor",
    version="0.0",
    author="PANLab team",
    author_email="pstetz@stanford.edu",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/WilliamsPANLab/eegor",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=1.18.1",
        "pandas>=0.23.4",
        "tqdm>=4.31.1",
        "scipy>=1.4.1",
        "mne>=0.23.0",
        "autoreject>=0.2.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3", # attention is 3.6.9
)
