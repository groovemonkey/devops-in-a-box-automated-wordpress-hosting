import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
# from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


MODULE_PATH = '/path/to/mymodules'


# A combination of the following docs:
## http://docs.ansible.com/ansible/latest/dev_guide/developing_api.html#python-api-2-0
## https://stackoverflow.com/questions/35368044/how-to-use-ansible-2-0-python-api-to-run-a-playbook


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


class TL_Ansible_Playbook(object):
    def __init__(self, playbook_path, host_list, inventory_file, extravars= {}, remote_user='root'):
        #         super(TL_Ansible_Playbook, self).__init__()
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
        # initialize needed objects
        self.loader = DataLoader()
        self.options = Options(connection='local', module_path=MODULE_PATH, forks=100, become=None, become_method=None, become_user=None, check=False,
                          diff=False, remote_user=remote_user)
        self.passwords = dict(vault_pass='secret')

        # Instantiate our ResultCallback for handling results as they come in
        self.results_callback = ResultCallback()

        # create inventory and pass to var manager
        self.inventory = InventoryManager(loader=self.loader, sources=[inventory_file])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.variable_manager.extra_vars = extravars

        ## CUSTOM PLAY with tasks
        # play_source =  dict(
        #         name = "Ansible Play",
        #         hosts = 'localhost',
        #         gather_facts = 'no',
        #         tasks = [
        #             dict(action=dict(module='shell', args='ls'), register='shell_out'),
        #             dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
        #          ]
        #     )
        # self.play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        self.playbook_path = playbook_path

        if not os.path.exists(playbook_path):
            print('[INFO] The playbook does not exist')
            sys.exit()


    def run(self):
        """Actually run it"""
        pbex = PlaybookExecutor(playbooks=[self.playbook_path], inventory=self.inventory,
                                variable_manager=self.variable_manager, loader=self.loader, options=self.options, passwords=self.passwords)
        results = pbex.run()

        ## CUSTOM PLAY with tasks
        # tqm = None
        # try:
        #     tqm = TaskQueueManager(
        #               inventory=self.inventory,
        #               variable_manager=self.variable_manager,
        #               loader=self.loader,
        #               options=self.options,
        #               passwords=self.passwords,
        #               stdout_callback=self.results_callback,  # Use our custom callback instead of the ``default`` callback plugin
        #           )
        #     result = tqm.run(self.play)
        # finally:
        #     if tqm is not None:
        #         tqm.cleanup()


class OLDDDD_TL_Ansible_Playbook(object):
    """
    A custom Ansible Playbook class that hooks into the Ansible API.
    We just want to be able to trigger playbook runs from Python.
    """

    def __init__(self, playbook_path, host_list, extravars= {}, remote_user='root'):
        super(TL_Ansible_Playbook, self).__init__()

        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader,  host_list=host_list)

        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.playbook_path = playbook_path

        if not os.path.exists(playbook_path):
            print('[INFO] The playbook does not exist')
            sys.exit()

        self.Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks', 'remote_user', 'private_key_file',
                                              'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
        self.options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100, remote_user=remote_user, private_key_file=None,
                               ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=None, check=False)

        # This can accomodate various other command line arguments.`
        self.variable_manager.extra_vars = extravars
        self.passwords = {}


    def execute(self):
        """
        Actually run this playbook.
        """
        pbex = PlaybookExecutor(playbooks=[self.playbook_path], inventory=self.inventory,
                                variable_manager=self.variable_manager, loader=self.loader, options=self.options, passwords=self.passwords)
        results = pbex.run()




