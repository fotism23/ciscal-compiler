run-default:
	python src/ciscal.py -i input.txt -o output.txt
	rm	src/*.pyc

run:
	python src/ciscal.py ${ARGS}
	rm	src/*.pyc

clean-pyc:
	find . -name 'src/*.pyc' -exec rm --force {} +
	find . -name 'src/*.pyo' -exec rm --force {} +
	find . -name 'src/*~' -exec rm --force  {} +

clean:
	rm	src/*.pyc
