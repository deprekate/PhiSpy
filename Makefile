env_dir:=venv
pip:=$(env_dir)/bin/pip

install:
	python3 -m venv $(env_dir)
	$(pip) install -r requirements.txt --process-dependency-links
	$(pip) install --upgrade pip

clean:
	rm -r $(env_dir)

reinstall:
	make clean install
