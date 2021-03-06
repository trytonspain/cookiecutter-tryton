#!/usr/bin/env python
# This file is part {{ cookiecutter.module_name }} module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from setuptools import setup
import re
import os
import io
from configparser import ConfigParser

{%- if cookiecutter.prefix %}

MODULE2PREFIX = {}
{%- endif %}


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


def get_require_version(name):
    if minor_version % 2:
        require = '%s >= %s.%s.dev0, < %s.%s'
    else:
        require = '%s >= %s.%s, < %s.%s'
    require %= (name, major_version, minor_version,
        major_version, minor_version + 1)
    return require

config = ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
version = info.get('version', '0.0.1')
major_version, minor_version, _ = version.split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)
name = '{{ cookiecutter.package_name }}'
download_url = 'https://bitbucket.org/{{ cookiecutter.download }}/trytond-{{ cookiecutter.module_name }}'

requires = []
for dep in info.get('depends', []):
    if not re.match(r'(ir|res)(\W|$)', dep):
{%- if not cookiecutter.prefix %}
        requires.append(get_require_version('trytond_%s' % dep))
{% else %}
        prefix = MODULE2PREFIX.get(dep, 'trytond')
        requires.append(get_require_version('%s_%s' % (prefix, dep)))
{% endif -%}
requires.append(get_require_version('trytond'))

{% if cookiecutter.test_with_scenario == 'y' -%}
tests_require = [get_require_version('proteus')]
{%- else -%}
tests_require = []
{%- endif %}
dependency_links = []
if minor_version % 2:
    # Add development index for testing with proteus
    dependency_links.append('https://trydevpi.tryton.org/')

setup(name=name,
    version=version,
    description='Tryton {{ cookiecutter.description or cookiecutter.module_name.replace('_', ' ').title() }} Module',
    long_description=read('README'),
    author='{{ cookiecutter.author }}',
    author_email='{{ cookiecutter.author_email }}',
    url='{{ cookiecutter.url }}',
    download_url=download_url,
    keywords='{{ cookiecutter.keywords }}',
    package_dir={'trytond.modules.{{ cookiecutter.module_name }}': '.'},
    packages=[
        'trytond.modules.{{ cookiecutter.module_name }}',
        'trytond.modules.{{ cookiecutter.module_name }}.tests',
        ],
    package_data={
        'trytond.modules.{{ cookiecutter.module_name }}': (info.get('xml', [])
            + ['tryton.cfg', 'view/*.xml', 'locale/*.po', '*.odt',
                'icons/*.svg', 'tests/*.rst']),
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Catalan',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business',
        ],
    license='GPL-3',
    install_requires=requires,
    dependency_links=dependency_links,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    {{ cookiecutter.module_name }} = trytond.modules.{{ cookiecutter.module_name }}
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    tests_require=tests_require,
    use_2to3=True,
{%- if cookiecutter.test_with_scenario == 'y' %}
    convert_2to3_doctests=['tests/scenario_{{ cookiecutter.module_name }}.rst'],
{%- endif %}
    )
