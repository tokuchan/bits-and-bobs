from setuptools import setup

setup(
    name = "nameit",
    version = "0.1.0",
    py_modules = ["nameit"],
    install_requires = [
        "click",
        "click-log",
    ],
    packages = ["words",],
    entry_points = '''
        [console_scripts]
        nameit=nameit:cli
    ''',
)
