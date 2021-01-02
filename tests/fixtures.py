import pytest
import json
import os
from tests.services.json_place_holder_service import JsonPlaceHolderService


@pytest.fixture(scope='session')
def test_config() -> json:
    config_file_name = 'config.json'
    config_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    config_file_name)
    with open(config_file_name) as fp:
        conf = json.load(fp)
    if os.getenv('environment') == 'local':
        env_conf = conf.get('local')
    else:
        env_conf = conf.get('prod')
    return env_conf


@pytest.fixture(scope='function')
def service_obj(test_config) -> JsonPlaceHolderService:
    return JsonPlaceHolderService(url=test_config.get("url"))

