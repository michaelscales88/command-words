# ML setup script
# Command: sudo -H make
.phony: clean base trainer api root_install
base="sphinxbase-5prealpha"
trainer="sphinxtrain-5prealpha"
api="pocketsphinx-5prealpha"

startup: setup.sh root_install
	sh setup.sh
	rm -f sphinx/*.tar.gz

root_install:
	apt install -y gcc automake autoconf libtool libasound2-dev \
	bison swig python-dev python3-dev libpulse-dev python-pyaudio \
	python3-pyaudio portaudio19-dev
	apt update
	apt upgrade

clean:
	rm -rf sphinx/

