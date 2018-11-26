sphinxbase="sphinxbase-5prealpha"
sphinxbasetar="$sphinxbase.tar.gz"
if [ ! -f "$sphinxbasetar" ] && [ ! -d "$sphinxbase" ]; then
   wget https://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/$sphinxbasetar
   xar -xvf "$sphinxbasetar"
fi

pocketsphinx="pocketsphinx-5prealpha"
pocketsphinxtar="$pocketsphinx.tar.gz"
if [ ! -f "$pocketsphinxtar" ] && [ ! -d "$pocketsphinx" ]; then
   wget https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/$pocketsphinxtar
   xar -xvf "$pocketsphinxtar"
fi
sphinxtrain="sphinxtrain-5prealpha"
sphinxtraintar="$sphinxtrain.tar.gz"
if [ ! -f "$sphinxtraintar" ] && [ ! -d "$sphinxtrain" ]; then
   wget https://sourceforge.net/projects/cmusphinx/files/sphinxtrain/5prealpha/$sphinxtraintar
   xar -xvf "$sphinxtraintar"
fi

