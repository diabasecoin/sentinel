import pytest
import os
import sys
import re

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), "../../lib")))
import config
from diabase_config import DiabaseConfig


def diabase_conf(**kwargs):
    defaults = {
        "rpcuser": "diabaserpc",
        "rpcpassword": "EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk",
        "rpcport": 29241,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(
        **defaults
    )

    return conf


def test_get_rpc_creds():
    diabase_config = diabase_conf()
    creds = DiabaseConfig.get_rpc_creds(diabase_config)

    for key in ("user", "password", "port"):
        assert key in creds
    assert creds.get("user") == "diabaserpc"
    assert creds.get("password") == "EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk"
    assert creds.get("port") == 29241

    diabase_config = diabase_conf(rpcpassword="s00pers33kr1t", rpcport=8000)
    creds = DiabaseConfig.get_rpc_creds(diabase_config)

    for key in ("user", "password", "port"):
        assert key in creds
    assert creds.get("user") == "diabaserpc"
    assert creds.get("password") == "s00pers33kr1t"
    assert creds.get("port") == 8000

    no_port_specified = re.sub("\nrpcport=.*?\n", "\n", diabase_conf(), re.M)
    creds = DiabaseConfig.get_rpc_creds(no_port_specified)

    for key in ("user", "password", "port"):
        assert key in creds
    assert creds.get("user") == "diabaserpc"
    assert creds.get("password") == "EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk"
    assert creds.get("port") == 17675


def test_slurp_config_file():
    import tempfile

    diabase_config = """# basic settings
#testnet=1 # TESTNET
server=1
printtoconsole=1
txindex=1 # enable transaction index
"""

    expected_stripped_config = """server=1
printtoconsole=1
txindex=1 # enable transaction index
"""

    with tempfile.NamedTemporaryFile(mode="w") as temp:
        temp.write(diabase_config)
        temp.flush()
        conf = DiabaseConfig.slurp_config_file(temp.name)
        assert conf == expected_stripped_config
