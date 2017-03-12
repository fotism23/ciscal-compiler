run-def:
	python src/ciscal.py -i input.cis -o output.out

run:
	python src/ciscal.py ${ARGS}

clean:
	rm	src/*.pyc

help:
	python src/ciscal.py -h
	rm src/*.pyc

debug:
	python src/ciscal.py -d -i input.cis -o output.out
	rm	src/*.pyc
