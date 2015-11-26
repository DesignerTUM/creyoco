from fabric.api import *

env.use_ssh_config = True
# env.hosts = ['creyoco_dev', 'creyoco_test']
env.hosts = ['creyoco']
env.code_dir = '/home/medienzentrum/creyoco/'
env.python_path = '/home/medienzentrum/.virtualenvs/creyoco/bin/python'


def pull():
    with cd(env.code_dir):
        run('git stash')
        run('git pull')
        run('git stash pop')


def push():
    local('git push')


def collectstatic():
    with cd(env.code_dir):
        run("{} manage.py collectstatic --noinput --settings=exedjango.deployment_settings".format(env.python_path))


def copy_site():
    run("sudo ln -sf {0}/apache/001-creyoco /etc/apache2/sites-enabled/".format(
        env.code_dir))


def restart():
    run("kill -HUP $(cat /tmp/creyoco.pid)")


def update():
    execute(push)
    execute(pull)
    execute(collectstatic)
    execute(restart)
