from keystoneclient.v3.projects import Project, ProjectManager


class TransactionProjectCreator(Project):

    def __init__(self, **kwargs):
        self.client = kwargs['client']
        self.project_name = kwargs['project_name']
        self.domain_id = kwargs['domain_id']

    def __enter__(self):
        self.project = self.client.projects.create(self.project_name,
                                                   self.domain_id)
        return self.project

    def __exit__(self, type, value, traceback):
        if value is not None:
            self.client.projects.delete(self.project.id)
