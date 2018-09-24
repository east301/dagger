# Dagger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dagger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dagger.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012 Remik Ziemlinski
# Copyright 2018 east301

from distutils.core import setup

setup(
    name='dagger-python3',
    version='1.3.0',
    author='Remik Ziemlinski',
    author_email='first.surname@gmail',
    packages=['dagger'],
    url='http://pythondagger.sourceforge.net/',
    license='GPL',
    description='File dependency graph evaluator.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools'
    ]
)
