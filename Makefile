.phony: clean base trainer api
base="sphinxbase-5prealpha"
trainer="sphinxtrain-5prealpha"
api="pocketsphinx-5prealpha"

startup: setup.sh
	sh setup.sh
	rm -f *.tar.gz

clean:
	rm -rf *.tar.gz $(base) $(trainer) $(api)

