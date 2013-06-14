#!/bin/bash
source ~/.bashrc
PROJECT_DIR=~/creyoco/
DJANGO_PATH=$PROJECT_DIR/src/exedjango/
LOGFILE=$PROJECT_DIR/log/creyoco.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=5
USER=$(whoami)
GROUP=$USER

workon creyoco
test -d $LOGDIR || mkdir -p $LOGDIR
touch $LOGFILE
cd $DJANGO_PATH
gunicorn_django -w $NUM_WORKERS --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE
echo "Gunicorn started"
