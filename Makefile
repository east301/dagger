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

.PHONY: clean dist html test

APP = pythondagger
DEVDIR = $(APP)-code

clean:
	cd bench && $(MAKE) -i clean
	cd doc && $(MAKE) -i clean
	cd test && $(MAKE) -i clean
	find . \( -name "*~" -o -name "*.pyc" \) -exec rm "{}" \;

dist:
  ifndef VER
		@echo "Error: VER is not defined. Try: make dist VER=1.0.0"
  else
		cd ..; rm -fr $(APP)-$(VER); mkdir $(APP)-$(VER); rsync --cvs-exclude -a $(DEVDIR)/ $(APP)-$(VER); tar zcvf $(APP)-$(VER).tar.gz $(APP)-$(VER); rm -fr $(APP)-$(VER);
  endif

html:
	cd doc && $(MAKE) html

pypi:
	python setup.py register sdist bdist_wininst upload
	-rm -fr MANIFEST build dist

pypidocs:
	cd doc/_build/html; zip -r /tmp/docs.zip *

test:
	cd test && $(MAKE) test
