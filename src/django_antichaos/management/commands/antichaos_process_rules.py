from optparse import make_option

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model

from django_antichaos.utils import process_commands

class Command(BaseCommand):
    help = "Loads rules from the file and apply them to given model's tags."
    args = "rules.csv [rules.csv ...]"
    option_list = BaseCommand.option_list + (
        make_option('--model', dest='model',
            help='Full model name in form "app_label.model".'),
    )
    requires_model_validation = True

    def handle(self, *files, **options):
        label = options.get('model')
        if label is None:
            raise CommandError('Please, specify model.')

        if not files:
            raise CommandError('Please, give me one or more files with commands.')

        model = get_model(*label.split('.', 1))
        if model is None:
            raise CommandError('Model "%s" not found.' % label)
        ctype = ContentType._default_manager.get_for_model(model)

        for file in files:
            print 'Processing commands from "%s"' % file
            process_commands(ctype, open(file).readlines())
        print 'Done'

