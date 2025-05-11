docker container prune -f
docker rmi -f python-test
docker build -t python-test .
docker run -it --rm \
    --env DISPLAY=$DISPLAY \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \
    --name python \
    python-test