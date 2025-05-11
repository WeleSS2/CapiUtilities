docker container prune -f
docker rmi python-test
docker build -t python-test .
docker container create -i -t --name python python-test
docker container start --attach -i python