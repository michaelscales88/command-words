base="sphinxbase-5prealpha.tar.gz"
if [ -f "$base" ]
	wget `https://sourceforge.net/projects/cmusphinx/${base}`
fi
pocketsphinx="pocketsphinx-5prealpha.tar.gz"
if [ -f "$pocketsphinx" ]
	wget `https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/${pocketsphinx}`
fi
sphinxtrain="sphinxtrain-5prealpha.tar.gz"
if [ -f "$sphinxtrain" ]
	wget `https://sourceforge.net/projects/cmusphinx/files/sphinxtrain/5prealpha/${sphinxtrain}`
fi

