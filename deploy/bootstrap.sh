#!/bin/bash

set -e

ssh root@hltv-parser.com bash -c '
  set -e
  apt-get update
  apt-get install -y socat apt-transport-https ca-certificates curl gnupg-agent software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  apt-get update
  apt-get install -y docker-ce docker-ce-cli containerd.io
  [ ! -d .acme.sh ] && curl https://get.acme.sh | sh
  ./.acme.sh/acme.sh --issue --standalone -d hltv-parser.com --force
  mkdir -p certs
  ./.acme.sh/acme.sh --install-cert -d hltv-parser.com --cert-file certs/cert.pem --key-file certs/key.pem --fullchain-file certs/fullchain.pem
  mkdir -p media
'

[ -z $(docker-machine ls --filter 'NAME=hltv-parser.com' -q) ] && docker-machine create --driver generic --generic-ip-address=hltv-parser.com --generic-ssh-user=root --generic-ssh-key ~/.ssh/id_rsa hltv-parser.com

./deploy/deploy.sh

ssh root@hltv-parser.com bash -c '
  set -e
  ./.acme.sh/acme.sh --remove -d hltv-parser.com
  mkdir -p acme-challenges
  ./.acme.sh/acme.sh --issue -d hltv-parser.com -w acme-challenges/
'
