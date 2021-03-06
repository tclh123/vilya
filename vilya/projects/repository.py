# -*- coding: utf-8 -*-

import os
from ..libs.git import Repository
from ..libs.text import format_md_or_rst
from ..settings import REPO_PATH
from .commit import Commit

REPO_ROOT_PATH = REPO_PATH


class ProjectRepository(Repository):

    def __init__(self, project):
        path = os.path.join(REPO_ROOT_PATH, project.path)
        self.project = project
        super(ProjectRepository, self).__init__(path)

    @classmethod
    def init(self, path, bare=True):
        path = os.path.join(REPO_ROOT_PATH, path)
        super(ProjectRepository, self).init(path, bare=bare)

    def get_commit(self, reference):
        pass

    def get_readme(self, reference='HEAD', path=None):
        entries = self.repository.list_entries(reference=reference,
                                               path=path)
        for path in entries:
            entry = entries[path]
            if (entry.is_blob and entry.name == 'README' or entry.name.startswith('README.')):
                readme_content = self.get_file(reference, path)
                return format_md_or_rst(path, readme_content)
        return ''

    def get_rendered_file(self, reference='HEAD', path=None):
        content = self.get_file(reference=reference, path=path)
        if content:
            return format_md_or_rst(path, content)

    def fork(self, path):
        path = os.path.join(REPO_ROOT_PATH, path)
        return self.repository.clone_to(path, bare=True)

    def list_commits(self, *k, **kw):
        commits = super(ProjectRepository, self).list_commits(*k, **kw)
        return [Commit(c) for c in commits]

    def resolve_commit(self, *k, **kw):
        commit = super(ProjectRepository, self).resolve_commit(*k, **kw)
        return Commit(commit) if commit else None
