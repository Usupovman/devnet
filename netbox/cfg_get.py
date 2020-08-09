# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True,
                  lstrip_blocks=True)
template = env.get_template('router_os_tempate.txt')


with open('data_yaml/R001.yaml') as f:
    routers = yaml.safe_load(f)

r1_conf = 'config/router_os/' + routers['name'] + '_config.txt'
print(r1_conf)
with open(r1_conf, 'w') as f:
    f.write(template.render(routers))
