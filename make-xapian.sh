#!/usr/bin/env bash

sudo aptitude install zlib1g-dev g++

export VENV=$VIRTUAL_ENV
mkdir $VENV/packages;
cd $VENV/packages;
rm xapian*;

curl http://oligarchy.co.uk/xapian/1.2.16/xapian-core-1.2.16.tar.xz | tar xJ;
curl http://oligarchy.co.uk/xapian/1.2.16/xapian-bindings-1.2.16.tar.xz  | tar xJ;

ls;
read;

pushd xapian-core*;
./configure --prefix=$VENV && make && make install;

export LD_LIBRARY_PATH=$VENV/lib;
popd; pushd xapian-bin*; 
./configure --prefix=$VENV --with-python && make && make install;

python -c "import xapian"; read;
