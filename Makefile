# ML setup script
# Command: sudo -H make
exe=execute_training.sh
setup=setup.sh

# Vars
.phony: clean base trainer api root_install startup sphinx_dir \
	clear_training_data clear_sphinx_data clear_training_folder \
	training_dir setup_training setup en_us
en_us=cmusphinx-en-us-ptm-5.2
sphinx_dir=sphinx
training_dir=data

run: $(exe)
	./$<

startup: $(setup) root_install
	./$<
	$(MAKE) setup_training
	pocketsphinx_mdef_convert -text $(training_dir)/en-us/mdef \
		$(training_dir)/en-us/mdef.txt
	rm -f $(sphinx_dir)/*.tar.gz

root_install:
	apt install -y gcc automake autoconf libtool libasound2-dev \
	bison swig python-dev python3-dev libpulse-dev python-pyaudio \
	python3-pyaudio portaudio19-dev
	apt update
	apt upgrade -y

setup_training:
	cp -a $(sphinx_dir)/$(en_us) $(training_dir)/en-us
	cp -a $(training_dir)/en-us $(training_dir)/en-us-adapt
	cp -a /usr/local/share/pocketsphinx/model/en-us/cmudict-en-us.dict $(training_dir)
	cp -a /usr/local/share/pocketsphinx/model/en-us/en-us.lm.bin $(training_dir)
	cp -a /usr/local/libexec/sphinxtrain/bw $(training_dir)
	cp -a /usr/local/libexec/sphinxtrain/map_adapt $(training_dir)
	cp -a /usr/local/libexec/sphinxtrain/mk_s2sendump $(training_dir)

clear_training_folder:
	rm -rf $(training_dir)

clear_training_data:
	find $(training_dir) -maxdepth 1 \
	! -name 'en-us' \
	! -name 'cmudict-en-us.dict' \
	! -name 'en-us.lm.bin' \

clear_sphinx_data:
	rm -rf $(sphinx_dir)

clean: clear_training_data clear_sphinx_data clear_training_folder
