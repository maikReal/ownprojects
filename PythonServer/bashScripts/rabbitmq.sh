sudo apt-get update 
sudo apt-get -y update 
echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list 
curl http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | sudo apt-key add - 
sudo apt-get update 
sudo apt-get install rabbitmq-server 
