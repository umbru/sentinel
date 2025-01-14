import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from umbrud import UmbruDaemon
from umbru_config import UmbruConfig


def test_umbrud():
    config_text = UmbruConfig.slurp_config_file(config.umbru_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000cb7859c07ebc3950ff150f5d6dc31150c5da14435fbf200d51be8f4208f'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = UmbruConfig.get_rpc_creds(config_text, network)
    umbrud = UmbruDaemon(**creds)
    assert umbrud.rpc_command is not None

    assert hasattr(umbrud, 'rpc_connection')

    # Umbru testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = umbrud.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert umbrud.rpc_command('getblockhash', 0) == genesis_hash
