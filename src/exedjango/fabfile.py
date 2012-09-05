from fabric.api import *

env.use_ssh_config = True
env.hosts = ['creyoco_dev']
env.code_dir = '/home/dimitri/creyoco/src/exedjango/'


def pull():
    with cd(env.code_dir):
        run('git pull')
        
def push():
    local('git push')
    
def update():
    execute(push)
    execute(pull)