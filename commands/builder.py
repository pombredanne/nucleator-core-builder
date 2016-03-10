# Copyright 2015 47Lining LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nucleator.cli.utils import ValidateCustomerAction
from nucleator.cli.command import Command
from nucleator.cli import properties
from nucleator.cli import ansible

import os, subprocess

class Builder(Command):
    
    name = "builder"
    
    def parser_init(self, subparsers):
        """
        Initialize parsers for this command.
        """

        # add parser for builder command
        builder_parser = subparsers.add_parser('builder')
        builder_subparsers=builder_parser.add_subparsers(dest="subcommand")

        # provision subcommand
        builder_provision=builder_subparsers.add_parser('provision', help="provision a new nucleator builder stackset")
        builder_provision.add_argument("--customer", required=True, action=ValidateCustomerAction, help="Name of customer from nucleator config")
        builder_provision.add_argument("--cage", required=True, help="Name of cage from nucleator config")

        # configure subcommand
        builder_provision=builder_subparsers.add_parser('configure', help="configure provisioned nucleator builder stackset")
        builder_provision.add_argument("--customer", required=True, action=ValidateCustomerAction, help="Name of customer from nucleator config")
        builder_provision.add_argument("--cage", required=True, help="Name of cage from nucleator config")

        # delete subcommand
        builder_delete=builder_subparsers.add_parser('delete', help="delete a previously provisioned nucleator builder stackset")
        builder_delete.add_argument("--customer", required=True, action=ValidateCustomerAction, help="Name of customer from nucleator config")
        builder_delete.add_argument("--cage", required=True, help="Name of cage from nucleator config")

        # keypair_sync subcommand
        builder_kpsynch=builder_subparsers.add_parser('keypair_sync', help="synchronize keypair files (*.pem) between local machine and nucleator")
        builder_kpsynch.add_argument("--customer", required=True, action=ValidateCustomerAction, help="Name of customer from nucleator config")
        builder_kpsynch.add_argument("--cage", required=True, help="Name of cage from nucleator config")


    def provision(self, **kwargs):
        """
        Provisions a Stackset that includes Nucleator, Jenkins and Artifactory instances 
        that can be used to implement a build / test / deploy workflow for one or more 
        applications.    
        """
        cli = Command.get_cli(kwargs)
        cage = kwargs.get("cage", None)
        customer = kwargs.get("customer", None)
        if cage is None or customer is None:
            raise ValueError("cage and customer must be specified")
        extra_vars={
            "cage_name": cage,
            "customer_name": customer,
            "cli_stackset_name": "builder",
            "cli_stackset_instance_name": "singleton",
            "verbosity": kwargs.get("verbosity", None),
            "debug_credentials": kwargs.get("debug_credentials", None),
        }

        extra_vars["builder_deleting"]=kwargs.get("builder_deleting", False) 

        command_list = []
        command_list.append("account")
        command_list.append("cage")
        command_list.append("builder")

        cli.obtain_credentials(commands = command_list, cage=cage, customer=customer, verbosity=kwargs.get("verbosity", None), debug_credentials=kwargs.get("debug_credentials", None))
        
        return cli.safe_playbook(self.get_command_playbook("builder_provision.yml"),
                                 is_static=True, # dynamic inventory not required
                                 **extra_vars
        )

    def configure(self, **kwargs):
        """
        Configures the Nucleator, Jenkins and Artifactory instances deployed by the 
        Builder Provision command.
        """
        cli = Command.get_cli(kwargs)
        cage = kwargs.get("cage", None)
        customer = kwargs.get("customer", None)
        if cage is None or customer is None:
            raise ValueError("cage and customer must be specified")
        extra_vars={
            "cage_name": cage,
            "customer_name": customer,
            "cli_stackset_name": "builder",
            "cli_stackset_instance_name": "singleton",
            "verbosity": kwargs.get("verbosity", None),
            "debug_credentials": kwargs.get("debug_credentials", None),
        }

        command_list = []
        command_list.append("builder")

        inventory_manager_rolename = "NucleatorBuilderInventoryManager"

        cli.obtain_credentials(commands = command_list, cage=cage, customer=customer, verbosity=kwargs.get("verbosity", None), debug_credentials=kwargs.get("debug_credentials", None)) # pushes credentials into environment

        return cli.safe_playbook(
            self.get_command_playbook("builder_configure.yml"),
            inventory_manager_rolename,
            **extra_vars
        )

    def delete(self, **kwargs):
        """
        This command deletes a previously provisioned Builder Stackset.
        """
        kwargs["builder_deleting"]=True
        return self.provision(**kwargs)

    def keypair_sync(self, **kwargs):
        """
        Synchronizing the keypair files locally to/from nucleator-ui, nucleator.
        """
        cli = Command.get_cli(kwargs)
        cage = kwargs.get("cage", None)
        customer = kwargs.get("customer", None)
        if cage is None or customer is None:
            raise ValueError("cage and customer must be specified")
        extra_vars={
            "cage_name": cage,
            "customer_name": customer,
            "verbosity": kwargs.get("verbosity", None),
            "debug_credentials": kwargs.get("debug_credentials", None),
        }

        command_list = []
        command_list.append("builder")

        inventory_manager_rolename = "NucleatorBuilderInventoryManager"

        cli.obtain_credentials(commands = command_list, cage=cage, customer=customer, verbosity=kwargs.get("verbosity", None), debug_credentials=kwargs.get("debug_credentials", None)) # pushes credentials into environment

        return cli.safe_playbook(
            self.get_command_playbook("rsync_pem.yml"),
            inventory_manager_rolename,
            **extra_vars
        )


# Create the singleton for auto-discovery
command = Builder()
