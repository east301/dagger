.PHONY: bench clean

bench:
	PYTHONPATH=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))/.. python bench.py --levels 5 --width 5 --dot tmp.dot

clean:
	rm -f tmp.* *~
