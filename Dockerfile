############################## Instructions ####################################
#install docker
#build container from the directory of this Dockerfile:  sudo docker build -rm --tag="creyoco" .  
#run: docker run -i -t creyoco  
#to stop all container: docker stop $(docker ps -a -q)
#to remove all container: docker rm $(docker ps -a -q)
################################################################################

FROM 	phusion/baseimage:0.9.11
MAINTAINER medienzentrum

# RUN		echo 'deb http://archive.ubuntu.com/ubuntu trusty main universe' > /etc/apt/sources.list
RUN 	apt-get update
RUN 	apt-get install -y python3-pip build-essential git openjdk-7-jre-headless libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev
RUN 	pip3 install virtualenv
RUN		virtualenv  creyocoenv
RUN 	cd creyocoenv
RUN		. /creyocoenv/bin/activate


RUN		rm -rf /home/creyoco
RUN 	git clone https://github.com/TUM-MZ/creyoco.git /home/creyoco/
RUN 	pip3 install -r /home/creyoco/pip-requirements.txt
RUN 	pip3 install -I pillow

EXPOSE 	8000
EXPOSE 	8080
WORKDIR /home/creyoco/
RUN 	python3.4 manage.py syncdb --noinput
RUN		python3.4 manage.py migrate exeapp --noinput
RUN     echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python3.4 manage.py shell --plain

RUN		python3.4 manage.py collectstatic --noinput

CMD 	python3.4 manage.py run_autobahn & python3.4 manage.py runserver 0.0.0.0:8000

