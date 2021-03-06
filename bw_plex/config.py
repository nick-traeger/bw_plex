import os
import configobj
from validate import Validator

vtor = Validator()

spec = """
url = string(default='')
token = string(default='')
verify_ssl = boolean(default=False)
servername = string(default='')
debug = boolean(default=False)

# Myplex username and password
username = string(default='')
password = string(default='')

logformat = ''
words = list(default=list('previously on', 'last season', 'last episode'))
# List of ratingkeys
ignore_show = list(default=list())

# Loglevel
level = string(default='debug')
# List of usernames, empty list allows all.
users = list(default=list())
# List of client names, empty list allows all
clients = list(default=list())
mode = string(default='skip_only_theme')
""".splitlines()


def migrate(conf):
    return conf


def read_or_make(fp):
    default = configobj.ConfigObj(None, configspec=spec,
                                  write_empty_values=True,
                                  create_empty=True,
                                  list_values=True)

    # Overwrite defaults options with what the user has given.
    if os.path.isfile(fp):
        config = configobj.ConfigObj(fp,
                                     write_empty_values=True,
                                     create_empty=True,
                                     list_values=True)
        default.merge(config)

    default.validate(vtor, copy=True)

    default = migrate(default)

    default.filename = fp
    default.write()
    return default
