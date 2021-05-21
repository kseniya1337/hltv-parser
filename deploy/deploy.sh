#!/bin/bash

set -e

eval $(docker-machine env hltv-parser.com)

docker-compose up --build -d
