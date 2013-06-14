#!/bin/bash
$GUNICORN_PATH=/home/medienzentrum/.virtualenvs/creyoco/bin/gunicorn_django
PID=/tmp/creyoco.pid
PROJECT_DIR=~/creyoco/
DJANGO_PATH=$PROJECT_DIR/src/exedjango/
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
    --pid $PID 2>$LOGFILE
echo "Gunicorn started"
