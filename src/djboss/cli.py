# -*- coding: utf-8 -*-

import logging
import os
import sys
import textwrap

from django.utils.importlib import import_module

from djboss.commands import Command


class SettingsImportError(ImportError):
    pass


def get_settings():
    cwd = os.getcwd()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.path.basename(cwd) + '.settings')
    sys.path.append(os.getcwd())
    try:
        from django.conf import settings
    except ImportError, exc:
        raise SettingsImportError(textwrap.dedent("""\
            Couldn't import a settings module. Make sure that the
            DJANGO_SETTINGS_MODULE environment variable points
            to a valid and importable Python module."""), exc)
    return settings


def find_commands(app):
    """Return a dict of `command_name: command_obj` for the given app."""

    commands = {}
    app_module = import_module(app) # Fail loudly if an app doesn't exist.
    try:
        commands_module = import_module(app + '.commands')
    except ImportError:
        pass
    else:
        for command in vars(commands_module).itervalues():
            if isinstance(command, Command):
                commands[command.name] = command
    return commands


def find_all_commands(apps):
    """Return a dict of `command_name: command_obj` for all the given apps."""

    commands = {}
    commands.update(find_commands('djboss'))
    for app in apps:
        commands.update(find_commands(app))
    return commands


def main():
    try:
        settings = get_settings()
    except SettingsImportError, exc:
        print >> sys.stderr, exc.args[0]
        print >> sys.stderr
        print >> sys.stderr, "The original exception was:"
        print >> sys.stderr, '\t' + str(exc.args[1])
        sys.exit(1)

    import django
    django.setup()
    commands = find_all_commands(settings.INSTALLED_APPS)

    from djboss.parser import PARSER

    PARSER.set_defaults(settings=settings)
    if settings.DEBUG:
        PARSER.set_defaults(log_level='DEBUG')
    else:
        PARSER.set_defaults(log_level='WARN')

    args = PARSER.parse_args()
    logging.root.setLevel(getattr(logging, args.log_level))

    # Call the command.
    commands[args.command](args)


if __name__ == '__main__':
    main()
