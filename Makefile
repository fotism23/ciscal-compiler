run-def:
	python src/ciscal.py -i input.ci -o output.asm

run:
	python src/ciscal.py ${ARGS}

clean:
	rm	src/*.pyc

help:
	python src/ciscal.py -h
	rm src/*.pyc

debug:
	python src/ciscal.py -d -i tests/input.ci -o output.asm
	rm	src/*.pyc

test:
    python src/ciscal.py -i tests/test1.ci -o test1.asm
    python src/ciscal.py -i tests/test2.ci -o test2.asm
    python src/ciscal.py -i tests/test3.ci -o test3.asm
    python src/ciscal.py -i tests/test4.ci -o test4.asm


