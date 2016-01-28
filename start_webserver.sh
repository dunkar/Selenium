#!/usr/bin/env bash

pushd _sampleWebpage
python3 -m http.server 8080
popd

