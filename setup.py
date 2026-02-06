from setuptools import setup
import json

with open("metadata.json", encoding="utf-8") as fp:
    metadata = json.load(fp)

setup(
    name="cldfbench_nawsawu2016makyam",
    py_modules=["cldfbench_nawsawu2016makyam"],
    include_package_data=True,
    url=metadata.get("url", ""),
    zip_safe=False,
    entry_points={
        "lexibank.dataset": [
            "nawsawu2016makyam=cldfbench_nawsawu2016makyam:Dataset",
        ]
    },
    install_requires=["pylexibank>=3.0.0"],
    extras_require={
        "test": [
            "pytest-cldf",
        ],
    },
)
