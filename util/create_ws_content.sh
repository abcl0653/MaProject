#!/usr/bin/env bash
# echo $1
mkdir ../website/questions/static/questions/workspaces/$1
pwd
cd ../website/questions/static/questions/workspaces/$1
pwd
cp ../../../../../../class/BHCexam1_simple.cls .
cp ../../../../../../header/question_artifact.tex ./$1.tex
cp ../../../../../../util/conv2jpg.py .
pwd
xelatex $1.tex
python3 conv2jpg.py
sublime ./$1.tex