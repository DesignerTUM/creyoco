#!/bin/bash
#start django_autobahn
#/home/medienzentrum/.virtualenvs/creyoco/bin/python /home/medienzentrum/creyoco/manage.py run_autobahn

#GUNICORN_PATH=/home/medienzentrum/.virtualenvs/creyoco/bin/gunicorn_django
gunicorn
PID=/tmp/creyoco.pid
PROJECT_DIR=~/creyoco/
DJANGO_PATH=$PROJECT_DIR
LOGFILE=$PROJECT_DIR/log/creyoco.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=5
USER=$(whoami)
GROUP=$USER

test -d $LOGDIR || mkdir -p $LOGDIR
touch $LOGFILE
cd $DJANGO_PATH
exec $GUNICORN_PATH -w $NUM_WORKERS --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE --pythonpath=. --settings=exedjango.deployment_settings \
    --pid $PID exedjango.aiohttp:app --worker-class aiohttp.GunicornWebWorker 2>$LOGFILE
echo "Gunicorn started"
