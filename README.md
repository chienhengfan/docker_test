this is easy docker exaple, merely use pandas to read csv( from kaggle) groupby and show

use ubuntu 18 to write Dockfile, and push to my dockerhub


在ubuntu上的操作(rf: https://docs.docker.com/language/python/build-images/)
  >>>1.write Dockerfile
  >>>
  >>>2.build image : sudo docker build --tag python-docker .
  >>>
  >>>3.see image : sudo docker images
  >>>
  >>>4.run docker on local : sudo docker run python-docker
  >>>
  >>>5.see alive docker container : sudo docker ps -a
  >>>
  >>>6.stop container : sudo docker stop "container id or names"(use docker ps -a to see)
