import argparse
import logging
import sys
import time

import epollServer as epoll

import utilities

__author__ = 'Ronak Kogta<rixor786@gmail.com>'
__description__ = ''' Foo proxy server '''

logger = logging.getLogger("foo_server")


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

def request_handler(epoll_context, parameters):
    request, _, _ = epoll_context
    request = request[:-1]
    try:
        req_type, seq = request.split(" ")
    except:
        req_type, seq, data = request.split(" ")

    if (req_type == "ACK" or req_type == "NAK"):
        return ""
        


    if (req_type == )    

if __name__ == '__main__':
        opts = argparse.ArgumentParser(description=__description__)
	parse_config(opts)
	args = opts.parse_args()

	config_dict = utilities.load_config(args.config)
	utilities.init_logger(logger, config_dict)
	check_config(config_dict, logger)
	

	server = epoll.Server(config_dict['server_port'], config_dict['host'], request_handler, [])
	server.run()
