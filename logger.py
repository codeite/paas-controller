
from common.config import Config
from api.resources.applications import Applications
from api.resources.globalconfig import GlobalConfig
import requests
import json
import threading

config = Config()
application = Applications(config)
globalconfig = GlobalConfig(config)

hosts = globalconfig.get('hosts')
apps = application.get_all()['data']

def container_host_logger(application, apps, host):
        r = requests.get('http://{}:8001/logs?colors=off'.format(host), stream=True)

        for line in r.iter_lines():
                if line:
                        for app in apps:
                                if app in line:
                                        node, log = line.split('|')
                                        application.write_container_logs(app, [ log ])

if __name__ == '__main__':
	host = hosts[0]
	threads = []
	for host in hosts:
		t = threading.Thread(target=container_host_logger, args=(application, apps, host))
		threads.append(t)
		t.start()
