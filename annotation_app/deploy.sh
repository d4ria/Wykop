#!/bin/bash

#file to be copied to AWS instance and building service

sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user

sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

yum install -y git
git clone https://github.com/doccano/doccano.git
cd doccano
sed -i s/"admin"/${username}/g docker-compose.prod.yml
sed -i s/"password"/${password}/g docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d
