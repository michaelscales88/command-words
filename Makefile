# ML setup script
# Command: sudo -H make
exe=execute_training.sh
setup=setup.sh
.phony: clean base trainer api root_install startup sphinx_dir \
	clear_training_data clear_sphinx_data clear_acoustic_model \
	training_dir copy_default_acoustic_model
sphinx_dir=sphinx
training_dir=data

run: $(exe)
	./$<

startup: $(setup) root_install
	./$<
	rm -f $(sphinx_dir)/*.tar.gz

root_install:
	apt install -y gcc automake autoconf libtool libasound2-dev \
	bison swig python-dev python3-dev libpulse-dev python-pyaudio \
	python3-pyaudio portaudio19-dev
	apt update
	apt upgrade -y

copy_default_acoustic_model: clear_acoustic_model
	cp -a /usr/local/share/pocketsphinx/model/en-us/en-us .
	cp -a /usr/local/share/pocketsphinx/model/en-us/cmudict-en-us.dict .
	cp -a /usr/local/share/pocketsphinx/model/en-us/en-us.lm.bin .

clear_acoustic_model:
	rm -rf en-us cmudict-en-us.dict en-us.lm.bin

clear_training_data:
	rm -rf $(training_dir)

clear_sphinx_data:
	rm -rf $(sphinx_dir)

clean: clear_training_data clear_sphinx_data clear_acoustic_model
