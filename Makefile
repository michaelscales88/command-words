.phony: clean base trainer api preinstall
base="sphinxbase-5prealpha"
trainer="sphinxtrain-5prealpha"
api="pocketsphinx-5prealpha"

startup: setup.sh
	sh setup.sh
	rm -f sphinx/*.tar.gz

root_install:
	apt install gcc automake autoconf libtool libasound2-dev \
		bison swig python-dev python3-dev libpulse-dev

clean:
	rm -rf sphinx/

