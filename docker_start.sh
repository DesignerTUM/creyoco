#!/bin/bash
# Run creyoco in the build docker container
creyoco_container=$1
: ${creyoco_container:=creyoco}
docker run -it -p 8000:8000 -p 8080:8080 $creyoco_container
