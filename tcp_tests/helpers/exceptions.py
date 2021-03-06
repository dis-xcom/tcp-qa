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


class UnexpectedExitCode(Exception):
    def __init__(self, command, ec, expected_ec, stdout=None, stderr=None):
        """Exception for unexpected exit code after executing shell/ssh command

        :param command: str - executed command
        :param ec: int - actual exit code
        :param expected_ec: list of integers - expected exit codes
        :param stdout: str
        :param stderr: str
        """
        self.ec = ec
        self.expected_ec = expected_ec
        self.cmd = command
        self.stdout = stdout
        self.stderr = stderr
        super(UnexpectedExitCode, self).__init__()

    def __str__(self):
        message = "Command '{cmd:s}' returned unexpected exit code {code:d}," \
                  " while waiting for {exp}".format(cmd=self.cmd,
                                                    code=self.ec,
                                                    exp=self.expected_ec)
        if self.stdout:
            message += "stdout: {}\n".format(self.stdout)
        if self.stderr:
            message += "stderr: {}\n".format(self.stderr)
        return message


class VariableNotSet(Exception):
    def __init__(self, variable_name, expected_value):
        self.variable_name = variable_name
        self.expected_value = expected_value
        super(VariableNotSet, self).__init__()

    def __str__(self):
        return "Variable {0} was not set in value {1}".format(
            self.variable_name, self.expected_value)


class DevopsConfigPathIsNotSet(ValueError):
    def __str__(self):
        return "Devops config/template path is not set!"


class DevopsConfigTypeError(TypeError):
    def __init__(self, type_name):
        self.type_name = type_name
        super(DevopsConfigTypeError, self).__init__()

    def __str__(self):
        return "Devops config should be dict instead of {0}".format(
            self.type_name
        )


class DevopsConfigIsNone(ValueError):
    def __str__(self):
        return "Devops config is None!"


class EnvironmentNameIsNotSet(ValueError):
    def __str__(self):
        return "Couldn't get environment name!"


class EnvironmentDoesNotExist(BaseException):
    def __init__(self, env_name):
        super(EnvironmentDoesNotExist, self).__init__()
        self.env_name = env_name

    def __str__(self):
        return "Environment {0} does not exist!".format(
            self.env_name
        )


class EnvironmentAlreadyExists(BaseException):
    def __init__(self, env_name):
        super(EnvironmentAlreadyExists, self).__init__()
        self.env_name = env_name

    def __str__(self):
        return "Environment {0} already exists!".format(
            self.env_name
        )


class EnvironmentWrongStatus(BaseException):
    def __init__(self, env_name, env_expected_status, env_actual_status):
        super(EnvironmentWrongStatus, self).__init__()
        self.env_name = env_name
        self.env_expected_status = env_expected_status
        self.env_actual_status = env_actual_status

    def __str__(self):
        return ("Environment '{0}' has wrong status: "
                "expected '{1}', got: '{2}'"
                .format(self.env_name,
                        self.env_expected_status,
                        self.env_actual_status))


class EnvironmentBadStatus(BaseException):
    def __init__(self, env_name, env_expected_status,
                 env_actual_status, wrong_resources):
        super(EnvironmentBadStatus, self).__init__()
        self.env_name = env_name
        self.env_expected_status = env_expected_status
        self.env_actual_status = env_actual_status
        self.wrong_resources = wrong_resources

    def __str__(self):
        return ("Environment '{0}' has bad status: "
                "expected '{1}', got: '{2}'\n{3}"
                .format(self.env_name,
                        self.env_expected_status,
                        self.env_actual_status,
                        self.wrong_resources))


class EnvironmentSnapshotMissing(BaseException):
    def __init__(self, env_name, snapshot_name):
        super(EnvironmentSnapshotMissing, self).__init__()
        self.env_name = env_name
        self.snapshot_name = snapshot_name

    def __str__(self):
        return ("Environment '{0}' doesn't have requested snapshot '{1}'! "
                "Please create the snapshot manually or erase the environment."
                .format(self.env_name, self.snapshot_name))


class EnvironmentIsNotSet(BaseException):
    def __str__(self):
        return "Environment is not set!"


class BaseImageIsNotSet(BaseException):
    def __str__(self):
        return "Base image for creating VMs is not set!"


class SaltPillarError(BaseException):
    def __init__(self, minion_id, pillar, message=''):
        super(SaltPillarError, self).__init__()
        self.minion_id = minion_id
        self.pillar = pillar
        self.message = message

    def __str__(self):
        return ("Salt pillar '{0}' error on minion {1}: {2}"
                .format(self.minion_id, self.pillar, self.message))


class EnvironmentNodeIsNotStarted(BaseException):
    def __init__(self, node_name, message=''):
        super(EnvironmentNodeIsNotStarted, self).__init__()
        self.node_name = node_name
        self.message = message

    def __str__(self):
        return ("Cloud-init failed on node {0} with error: \n{1}"
                .format(self.node_name, self.message))


class EnvironmentNodeAccessError(BaseException):
    def __init__(self, node_name, message=''):
        super(EnvironmentNodeAccessError, self).__init__()
        self.node_name = node_name
        self.message = message

    def __str__(self):
        return ("Unable to reach the node {0}: \n{1}"
                .format(self.node_name, self.message))
