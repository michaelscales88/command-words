# ML setup script
# Command: sudo -H make
exe=execute_training.sh
setup=setup.sh

# Vars
.phony: clean base trainer api root_install startup sphinx_dir \
	clear_training_data clear_sphinx_data training_dir en_us setup \
	setup_training
en_us=cmusphinx-en-us-ptm-5.2
sphinx_dir=sphinx
training_dir=data

run: $(exe)
	./$<

startup: $(setup) root_install
	./$<
	$(MAKE) setup_training
	rm -f $(sphinx_dir)/*.tar.gz

root_install:
	apt install -y gcc automake autoconf libtool libasound2-dev \
	bison swig python-dev python3-dev libpulse-dev python-pyaudio \
	python3-pyaudio portaudio19-dev
	apt update
	apt upgrade -y

setup_training: clear_training_data
	cp -a $(sphinx_dir)/$(en_us) $(training_dir)/en-us
	pocketsphinx_mdef_convert -text $(training_dir)/en-us/mdef \
		$(training_dir)/en-us/mdef.txt
	cp -a $(training_dir)/en-us $(training_dir)/en-us-adapt
	cp -a /usr/local/share/pocketsphinx/model/en-us/cmudict-en-us.dict $(training_dir)
	cp -a /usr/local/share/pocketsphinx/model/en-us/en-us.lm.bin $(training_dir)
	cp -a /usr/local/libexec/sphinxtrain/bw $(training_dir)
	cp -a /usr/local/libexec/sphinxtrain/map_adapt $(training_dir)
	cp -a /usr/local/libexec/sphinxtrain/mk_s2sendump $(training_dir)

clear_training_data:
	mkdir -p $(training_dir)
	rm -rf $(training_dir)/*

clear_sphinx_data:
	mkdir -p $(sphinx_dir)
	rm -rf $(sphinx_dir)/*

clean: clear_training_data clear_sphinx_data
