apt update
mkdir mongodb
cd mongodb
apt install curl
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.4.7.tgz
tar xvf mongodb-linux-x86_64-3.4.7.tgz
mv mongodb-linux-x86_64-3.4.7 mongodb
cd mongodb
export PATH=$PATH:/home/journal/mongodb/mongodb/bin
mkdir data
cd bin
