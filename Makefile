TEMPFILE := $(shell mktemp -u)

.PHONY: install clean uninstall venv

install:
	python setup.py install

uninstall:
	python setup.py install --record ${TEMPFILE} && \
		cat ${TEMPFILE} | xargs rm -rf && \
		rm -f ${TEMPFILE}

venv:
	virtualenv venv && source venv/bin/activate && pip install -r requirements.txt
	@echo "Run 'source venv/bin/activate' to enter virtual environment and 'deactivate' to return from it"

clean:
	find . -name '*.pyc' -delete
	rm -rf venv
