import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="notalib",
	version="1.0.0",
	author="m1kc (Max Musatov)",
	author_email="m1kc@yandex.ru",
	description="A collection of utility functions & classes",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/m1kc/notalib",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
