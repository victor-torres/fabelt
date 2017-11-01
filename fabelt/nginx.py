from fabric.api import put, run, task

from fabelt import apt


@task
def install():
    # TODO: support other systems
    apt.install('nginx')


@task
def config():
    config = {
        'ports': ', '.join(env.server_ports),
        'server_names': ', '.join(env.server_names),
        'locations': [
            #
        ]
    }
    
    
