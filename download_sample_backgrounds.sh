#!/bin/bash

echo "Downloading sample videos"

wget https://github.com/fabian57fabian/genvid-minimal/releases/download/video2/backgrounds1.tar.xz
tar -xf backgrounds1.tar.xz -C backgrounds
rm backgrounds1.tar.xz

echo "Sample backgrounds downloaded"