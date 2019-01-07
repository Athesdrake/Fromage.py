import re
import setuptools

with open('fromage/__version__.py') as f:
	match = re.search(r'__version__ = (["\'])([^"\']+)\1', f.read())
	version = match.group(2)

with open('requirements.txt') as f:
	requirements = f.readlines()
with open('README.md') as f:
	description = f.read()

setuptools.setup(
	name='Fromage.py',
	version=version,
	packages=['fromage'],
	author='Athesdrake',
	description="Fromage.py is an API for the Atelier801's forums.",
	long_description=description,
	long_description_content_type='text/markdown',
	url='https://github.com/Athesdrake/Fromage.py',
	install_requires=requirements,
	python_requires='>=3.5.3',
	classifiers=[
		"Development Status :: 2 - Pre-Alpha",
		"Framework :: AsyncIO",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Topic :: Software Development :: Libraries",
	]
)