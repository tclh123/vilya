# -*- coding: utf-8 -*-

from datetime import datetime
from ..core import db
from .repository import Repository


class PullRequest(db.Model):
    __tablename__ = 'pullrequests'

    id = db.Column(db.Integer(), primary_key=True)
    issue_id = db.Column(db.Integer())
    origin_project_id = db.Column(db.Integer())
    origin_project_ref = db.Column(db.String(1024))
    upstream_project_id = db.Column(db.Integer())
    upstream_project_ref = db.Column(db.String(1024))
    origin_commit_sha = db.Column(db.String(40))
    upstream_commit_sha = db.Column(db.String(40))
    merged_commit_sha = db.Column(db.String(40))
    merger_id = db.Column(db.Integer())
    creator_id = db.Column(db.Integer())
    merged_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)


    def is_local(self):
        return self.origin_project_id == self.upstream_project_id

    @property
    def issue(self):
        from ..services import issues
        return issues.get(id=self.issue_id)

    @property
    def name(self):
        return self.issue.name

    @property
    def description(self):
        return self.issue.description

    @property
    def number(self):
        return self.issue.number

    @property
    def origin_project(self):
        from ..services import projects
        return projects.get(self.origin_project_id)

    @property
    def upstream_project(self):
        from ..services import projects
        return projects.get(self.upstream_project_id)

    @property
    def repository(self):
        return Repository(self)

    def after_create(self):
        self.repository.sync()
