# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from vilya.api import create_app
from vilya.manage import (CreateUserCommand,
                          DeleteUserCommand,
                          ListUsersCommand,
                          CreateProjectCommand,
                          DeleteProjectCommand,
                          ListProjectsCommand)

manager = Manager(create_app())
manager.add_command('create_user', CreateUserCommand())
manager.add_command('delete_user', DeleteUserCommand())
manager.add_command('list_users', ListUsersCommand())
manager.add_command('create_project', CreateProjectCommand())
manager.add_command('delete_project', DeleteProjectCommand())
manager.add_command('list_projects', ListProjectsCommand())

if __name__ == "__main__":
    manager.run()
