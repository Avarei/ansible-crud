#!/usr/bin/python
# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.playbook.helpers import load_list_of_tasks
from ansible.playbook.task import Task

class ActionModule(ActionBase):
    ''' TODO write Documentation '''

    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # deprecated

        validation_result, new_module_args = self.validate_argument_spec(
            argument_spec=dict(
                create=dict(type='list', required=False),
                read=dict(type='list', required=True),
                update=dict(type='list', required=False),
                delete=dict(type='list', required=False),
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
            create=dict(),
            read=dict(),
            update=dict(),
            delete=dict()
        )
        task = readActions[0]
        # load_list_of_tasks(ds=createActions, loader=self._loader, play=self._task.get_variable_manager()._play)
        task_result = self._execute_module(task, task_vars=task_vars)
        # task_result = self._execute_module(module_name=task.action, module_args=task.args, task_vars=task_vars)


        # result['read'] = task_result
        # result['read']['debug'] = task.action

        # module_args = self._task.args.copy()
        # return self._execute_module(module_name='ansible.builtin.file',
        #                                      module_args=dict(path='./hello.txt', state='touch'),
        #                                      task_vars=task_vars)




        # for action in readActions:
        #     # load task from action


        return result
