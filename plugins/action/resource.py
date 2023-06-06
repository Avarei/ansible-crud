#!/usr/bin/python
# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):
    ''' TODO write Documentation '''

    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # deprecated
        operation_args = dict(
            action = dict(type='str', required=True),
            args = dict(type='dict', required=False),
        )

        validation_result, new_module_args = self.validate_argument_spec(
            argument_spec=dict(
                create=dict(type='list', required=False, options=operation_args),
                read=dict(type='list', required=True, options=operation_args),
                update=dict(type='list', required=False, options=operation_args),
                delete=dict(type='list', required=False, options=operation_args),
                state=dict(
                    type='str',
                    choices=['present', 'absent', 'read', 'created'],
                    default='present'
                )
            ),
            required_if=[
                ['state', 'present', ('create',)],
                ['state', 'present', ('update',)],
                ['state', 'absent', ('delete',)],
                ['state', 'created', ('create',)],
            ]
        )

        createActions = new_module_args['create']
        readActions = new_module_args['read']
        updateActions = new_module_args['update']
        deleteActions = new_module_args['delete']
        state = new_module_args['state']

        result = dict(
            changed=False,
            create=[],
            read=[],
            update=[],
            delete=[]
        )
        task = readActions
        # todo check if task has action and args

        # result['read'] = self._execute_module(module_name=task['action'], module_args=task['args'], task_vars=task_vars)

        readResult = execute_module(self, readActions, task_vars)
        result['read'] = readResult

        # TODO determine if there was a exception
        # TODO determine if there was a resource exists

        if state in ['present', 'created']:

            if ('failed' in readResult and readResult['failed']) or readResult['rc'] != 0:
                result['create'] = execute_module(self, createActions, task_vars)
                if 'changed' in result['create']:
                    result['changed'] = result['create']['changed']
                if 'failed' in result['create']:
                    result['failed'] = result['create']['failed']
            elif state == 'present':
                # Resource Exists and state is present
                updateResult = execute_module(self, updateActions, task_vars)
                result['update'] = updateResult
                if ('failed' in updateResult and updateResult['failed']) or updateResult['rc'] != 0:
                    raise Exception('Update failed')

                if 'changed' in updateResult:
                    result['changed'] = updateResult['changed']
                if 'failed' in updateResult:
                    result['failed'] = updateResult['failed']
        elif state == 'absent':
            if not readResult['failed'] and readResult['rc'] != 0:
                result['delete'] = execute_module(self, deleteActions, task_vars)
                if 'changed' in result['delete']:
                    result['changed'] = result['delete']['changed']
                if 'failed' in result['delete']:
                    result['failed'] = result['delete']['failed']
            # else:
            #   No resource to delete



        return result

def execute_module(self, tasks, task_vars):
    results = []
    for task in tasks:
        if not 'action' in task or not 'args' in task:
            raise Exception('Action or args missing in task')

        results.append(self._execute_module(module_name=task['action'], module_args=task['args'], task_vars=task_vars))

    return results
