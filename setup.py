from setuptools import setup

setup(
    name="cldfbench_nawsawu2016makyam",
    version="1.0.0",
    description="CLDF dataset based on Nawsawu (2016) Descriptive Phonology of Makyam Naga",
    license="CC-BY-4.0",
    py_modules=["cldfbench"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "cldfbench.dataset": [
            "nawsawu2016makyam=cldfbench_nawsawu2016makyam:Dataset",
        ]
    },
    install_requires=[
        "cldfbench",
        "pycldf",
    ],
)
