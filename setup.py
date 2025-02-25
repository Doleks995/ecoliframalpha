from setuptools import setup, find_packages

setup(
    name="ecoliframalpha",
    version="1.1.0",
    author="David Oleksy, Rubén Crespo Blanco",
    author_email="rcresb@gmail.com, dao995@g.harvard.edu",
    description="Perform the simulation of translation dynamics accounting for degeneracy lifting.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Doleks995/ecoliframalpha?tab=readme-ov-file",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib", 
        "pytest",
        "scikit-learn",
        "scipy",
        "seaborn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
