import click
import datetime
import fnmatch
import logging
import requests
import sys


LOG = logging.getLogger(__name__)


class Settings(object):
    ipaddr = '192.168.1.1'
    port = 80
    user = 'admin'
    password = ''


@click.pass_context
def url_for(ctx, script):
    url = 'http://{addr}:{port}/{script}'.format(
        addr=ctx.obj.ipaddr, port=ctx.obj.port, script=script)

    LOG.debug('generated url "%s" for script "%s"',
              url, script)
    return url

@click.pass_context
def auth_params(ctx):
    return {'user': ctx.obj.user, 'pwd': ctx.obj.password}


@click.group()
@click.option('-i', '--ip', '--ipaddr', default='192.168.1.1')
@click.option('-p', '--port', default=80, type=int)
@click.option('-v', '--verbose', 'loglevel', flag_value='INFO')
@click.option('-d', '--debug', 'loglevel', flag_value='DEBUG')
@click.option('-u', '--user', default='admin')
@click.option('-p', '--password', default='')
@click.pass_context
def cli(ctx, ipaddr, port, user, password, loglevel='WARN'):
    ctx.obj = Settings()
    ctx.obj.ipaddr = ipaddr
    ctx.obj.port = port
    ctx.obj.user = user
    ctx.obj.password = password

    logging.basicConfig(level=loglevel)

    LOG.debug('using ipaddr %s, port %d', ctx.obj.ipaddr, ctx.obj.port)


@click.command()
@click.option('--output', '-o')
@click.pass_context
def snapshot(ctx, output):
    if output is None:
        now = datetime.datetime.now()
        output = 'snapshot-{}.jpg'.format(now.isoformat())

    res = requests.get(url_for('snapshot.cgi'),
                       params=dict(json=1, **auth_params()))

    res.raise_for_status()

    with open(output, 'w') as fd:
        fd.write(res.content)


@click.command()
@click.option('--output', '-o')
@click.argument('patterns', nargs=-1)
@click.pass_context
def get_params(ctx, output, patterns):
    res = requests.get(url_for('get_params.cgi'),
                       params=dict(json=1, **auth_params()))

    res.raise_for_status()
    data = res.json()
    selected = set()
    for pattern in patterns:
        matched = (set(fnmatch.filter(data.keys(), pattern)))
        selected = selected.union(matched)

    selected = selected or data.keys()

    with open(output, 'w') if output else sys.stdout as fd:
        click.echo('\n'.join("{} = {}".format(k, data[k])
                             for k in sorted(selected)),
                   file=fd)


@click.command()
@click.option('-n', '--nosave', is_flag=True)
@click.option('-r', '--reboot', is_flag=True)
@click.argument('pspec', nargs=-1)
@click.pass_context
def set_params(ctx, nosave, reboot, pspec):
    params = dict(x.split('=', 1) for x in pspec)
    params.update(auth_params())

    if not nosave:
        params['save'] = '1'

    if reboot:
        params['reboot'] = '1'

    res = requests.get(url_for('set_params.cgi'),
                       params=dict(**params))
    res.raise_for_status()

    click.echo('Configured.')


cli.add_command(snapshot)
cli.add_command(get_params)
cli.add_command(set_params)

if __name__ == '__main__':
    cli(auto_envvar_prefix='DRONECAM')
