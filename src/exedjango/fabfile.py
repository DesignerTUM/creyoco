from fabric.api import *

env.use_ssh_config = True
env.hosts = ['creyoco_dev', 'creyoco_test']
env.code_dir = '/home/dimitri/creyoco/src/exedjango'


def pull():
    with cd(env.code_dir):
        run('git pull')


def push():
    local('git push')


def update():
    execute(push)
    execute(pull)
    execute(restart)


def copy_site():
    run("sudo ln -sf {0}/apache/001-creyoco /etc/apache2/sites-enabled/".format(env.code_dir))


def restart():
    run("kill -HUP $(cat /tmp/creyoco.pid)")
