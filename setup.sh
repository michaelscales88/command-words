export LD_LIBRARY_PATH=/usr/local/lib
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig

SPHINX_DIR="sphinx"

mkdir -p "$SPHINX_DIR"

# Download and unpack required CMU sphinx libraries
sphinxbase="sphinxbase-5prealpha"
sphinxbasetar="$sphinxbase.tar.gz"
if [ ! -f "$SPHINX_DIR/$sphinxbasetar" ] && [ ! -d "$SPHINX_DIR/$sphinxbase" ]; then
   wget -P "$SPHINX_DIR/" https://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/$sphinxbasetar
   tar -xvf "$SPHINX_DIR/$sphinxbasetar" -C "$SPHINX_DIR/"
fi

pocketsphinx="pocketsphinx-5prealpha"
pocketsphinxtar="$pocketsphinx.tar.gz"
if [ ! -f "$SPHINX_DIR/$pocketsphinxtar" ] && [ ! -d "$SPHINX_DIR/$pocketsphinx" ]; then
   wget -P "$SPHINX_DIR/" https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/$pocketsphinxtar
   tar -xvf "$SPHINX_DIR/$pocketsphinxtar" -C "$SPHINX_DIR/"
fi
sphinxtrain="sphinxtrain-5prealpha"
sphinxtraintar="$sphinxtrain.tar.gz"
if [ ! -f "$SPHINX_DIR/$sphinxtraintar" ] && [ ! -d "$SPHINX_DIR/$sphinxtrain" ]; then
   wget -P "$SPHINX_DIR/" https://sourceforge.net/projects/cmusphinx/files/sphinxtrain/5prealpha/$sphinxtraintar
   tar -xvf "$SPHINX_DIR/$sphinxtraintar" -C "$SPHINX_DIR/"
fi

# Run package installation
if [ -d "$SPHINX_DIR/$sphinxbase" ]; then
   cd "$SPHINX_DIR/$sphinxbase"
   ./configure
   make
   make install
   cd ../..
fi
if [ -d "$SPHINX_DIR/$sphinxtrain" ]; then
   cd "$SPHINX_DIR/$sphinxtrain"
   ./configure
   make
   make install
   cd ../..
fi
if [ -d "$SPHINX_DIR/$pocketsphinx" ]; then
   cd "$SPHINX_DIR/$pocketsphinx"
   ./configure
   make
   make install
   cd ../..
fi

# Install the python requirements
python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt

