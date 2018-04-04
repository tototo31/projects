#!/bin/bash

current=$PWD

echo  "Updating compsci work"
if [ -d "$HOME/cmpsci122" ]
then
	cd $HOME/cmpsci122
	git pull
else
	echo "Cmpsci work not cloned or has a different name or is not installed in $HOME"
fi

echo "Updating dot-files"
if [ -d "$HOME/cmpsci122" ]
then
	cd $HOME/dot-files
	git pull
else
	echo "dot-files work not cloned or has a different name or is not installed in $HOME"
fi

echo "Updating Projects"
if [ -d "$HOME/projects" ]
then
	cd $HOME/projects
	git pull
else
	echo "projects not cloned or has a different name or is not installed in $HOME"
fi

echo "moving back to PWD"

cd $CURRENT
