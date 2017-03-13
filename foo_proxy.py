import argparse
import logging
import sys
import time
import signal

import epollServer as epoll

import utilities

__author__ = 'Ronak Kogta<rixor786@gmail.com>'
__description__ = ''' Foo proxy protocol '''

logger = logging.getLogger()


''' Handles cmdline argumets'''


def parse_config(opts):
    opts.add_argument('-c', '--config', help='Configuration file', default='config.json')

''' Check if configuration file is properly set'''

def check_config(config_dict, logger):
	sport = (type(config_dict['server_port']) == int)
	fport = (type(config_dict['proxy_port']) == int)
	log = (type(config_dict['log']) == unicode)
    host = (type(config_dict['host']) == unicode)
	
	if not (sport and fport and log and host):
		logger.error('%s is not correctly configured' % CONFIG_FILE)
		sys.exit(-1)


def proxy_request_handler(epoll_context, parameters):
	startTime = time.time()
	request, host, port = epoll_context
	

def server_request_handler(epoll_context, parameters):
    startTime = time.time()
    request, host, port = epoll_context
    	
def receive_signal(signum, stack):
    print 'Received:', signum


if __name__ == '__main__':
        opts = argparse.ArgumentParser(description=__description__)
	parse_config(opts)
	args = opts.parse_args()

	config_dict = utilities.load_config(args.config)
	utilities.init_logger(logger, config_dict)
	check_config(config_dict, logger)
	signal.signal(signal.SIGUSR1, receive_signal)

	#server = epoll.Server(int(args.port), args.host, request_handler, [])
	#thisserver.run()
