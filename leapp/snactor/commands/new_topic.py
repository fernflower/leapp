import os

import sys

from leapp.utils.repository import (make_class_name, make_name, find_repository_basedir,
                                    requires_repository)
from leapp.utils.clicmd import command_arg, command
from leapp.exceptions import CommandError

_LONG_DESCRIPTION = '''
Creates a new Topic in the current repository.

For more information please consider reading the documentation at:
https://red.ht/leapp-docs
'''


@command('new-topic', help='Creates a new topic')
@command_arg('topic-name')
@requires_repository
def cli(args):
    topic_name = args.topic_name
    basedir = find_repository_basedir('.')

    basedir = os.path.join(basedir, 'topics')
    if not os.path.isdir(basedir):
        os.mkdir(basedir)

    topic_path = os.path.join(basedir, topic_name.lower() + '.py')
    if os.path.exists(topic_path):
        raise CommandError("File already exists: {}".format(topic_path))

    topic_path = os.path.join(basedir, topic_name.lower() + '.py')
    topic_class_name = make_class_name(topic_name)
    if not topic_class_name.endswith('Topic'):
        topic_class_name += 'Topic'
    with open(topic_path, 'w') as f:
        f.write('''from leapp.topics import Topic


class {topic_name}(Topic):
    name = '{topic}'
'''.format(topic_name=topic_class_name, topic=make_name(topic_name)))

    sys.stdout.write("New topic {} has been created in {}\n".format(topic_class_name, os.path.realpath(topic_path)))
