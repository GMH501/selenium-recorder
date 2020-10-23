from setuptools import setup

setup(
    name="tester.sh",
    version="0.1",
    author="Gabriel Meghnagi",
    author_email="gabrielmeghnagi@outlook.it",
    url="https://github.com/GMH501/tester.git",
    include_package_data=True,
    install_requires=["flask", "setuptools", "psutil"],
    entry_points="""
        [console_scripts]
        tester=tester:run
    """,
    )
