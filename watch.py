from __future__ import print_function
from threading import Thread
import os

from invoke import task, run


@task
def coffee():
    run("coffee --watch")


@task
def guard():
    print(os.getcwd())
    run("guard")


@task
def sass():
    run("cd exeapp/static; compass watch --debug; cd -")


@task(default=True, name='watch')
def main():
    threads = map(lambda x: Thread(target=x), (sass, guard))
    [x.start() for x in threads]
    [x.join() for x in threads]

