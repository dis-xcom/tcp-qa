#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pytest

from tcp_tests import logger
from tcp_tests.helpers import ext
from tcp_tests.managers import drivetrain_manager

LOG = logger.logger


@pytest.fixture(scope='function')
def drivetrain_actions(config, underlay_actions, salt_actions):
    """Fixture that provides various actions for Drivetrain

    :param config: fixture provides oslo.config
    :param underlay: fixture provides underlay manager
    :rtype: DrivetrainManager
    """
    return drivetrain_manager.DrivetrainManager(config, underlay_actions,
                                                salt_actions)


@pytest.mark.revert_snapshot(ext.SNAPSHOT.drivetrain_deployed)
@pytest.fixture(scope='function')
def drivetrain_deployed(revert_snapshot, request, config,
                        hardware, underlay, salt_deployed,
                        drivetrain_actions):
    """Fixture to get or install Drivetrain on the environment

    :param revert_snapshot: fixture that reverts snapshot that is specified
                            in test with @pytest.mark.revert_snapshot(<name>)
    :param request: fixture provides pytest data
    :param config: fixture provides oslo.config
    :param hardware: fixture provides enviromnet manager
    :param underlay: fixture provides underlay manager
    :param drivetrain_actions: fixture provides OSSManager instance
    :rtype: DrivetrainManager

    If config.drivetrain.drivetrain_installed is not set, this
    fixture assumes that the Drivetrain were not installed
    , and do the following:
    - install Drivetrain
    - make snapshot with name 'drivetrain_deployed'
    - return DrivetrainManager

    If config.drivetrain.drivetrain_installed was set, this fixture
    assumes that the Drivetrain were already installed, and do
    the following:
    - return DrivetrainManager instance

    If you want to revert 'drivetrain_deployed' snapshot, please use mark:
    @pytest.mark.revert_snapshot("drivetrain_deployed")
    """
    if not config.drivetrain.drivetrain_installed:
        steps_path = config.drivetrain_deploy.drivetrain_steps_path
        commands = underlay.read_template(steps_path)
        drivetrain_actions.install(commands)
        hardware.create_snapshot(ext.SNAPSHOT.drivetrain_deployed)
        salt_deployed.sync_time()

    else:
        # 1. hardware environment created and powered on
        # 2. config.underlay.ssh contains SSH access to provisioned nodes
        #    (can be passed from external config with TESTS_CONFIGS variable)
        # 3. config.tcp.* options contain access credentials to the already
        #    installed TCP API endpoint
        pass

    return drivetrain_actions
