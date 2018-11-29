# ML setup script
# Command: sudo -H make
.phony: clean base trainer api root_install startup \
	clear_training_data clear_sphinx_data sphinx_dir \
	training_dir
exe=execute_training.sh
setup=setup.sh
sphinx_dir=sphinx
training_dir=data
base="sphinxbase-5prealpha"
trainer="sphinxtrain-5prealpha"
api="pocketsphinx-5prealpha"

run: $(exe)
	./$<

startup: $(setup) root_install
	./$<
	rm -f sphinx/*.tar.gz

root_install:
	apt install -y gcc automake autoconf libtool libasound2-dev \
	bison swig python-dev python3-dev libpulse-dev python-pyaudio \
	python3-pyaudio portaudio19-dev
	apt update
	apt upgrade -y

clear_training_data:
	rm -rf $(training_dir)

clear_sphinx_data:
	rm -rf $(sphinx_dir)

clean: clear_training_data clear_sphinx_data

