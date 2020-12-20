
install :
	sed 's?path?'$(shell pwd)'/autogenerator.py?' install/autogenerator > /usr/local/bin/autogenerator
	chmod a+x /usr/local/bin/autogenerator

.PHONY : install
