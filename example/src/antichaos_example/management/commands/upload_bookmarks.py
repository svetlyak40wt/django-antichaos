import logging
from optparse import make_option
from BeautifulSoup import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError
from antichaos_example.models import Link
from tagging.models import TaggedItem
from django_antichaos.utils import model_to_ctype


class Command(BaseCommand):
    help = "Load bookmarks from html file in Netscape Bookmarks format."
    option_list = BaseCommand.option_list + (
        make_option('--replace', action='store_true', dest='replace', default=False,
            help='Replace all links in database to links from file (default - don\'t replace).'),
        make_option('--limit', dest='limit', default=None,
            help='Limit number of links to upload.'),
    )

    def execute(self, *args, **options):
        if len(args) == 0:
            raise CommandError('Please, specify filename with bookmarks!')

        filename = args[0]
        limit = options.get('limit', None)
        replace = options.get('replace', False)

        soup = BeautifulSoup(open(filename))
        links = soup.findAll('a', attrs = dict(tags=lambda tag: tag))

        if replace:
            Link.objects.all().delete()
            ctype = model_to_ctype(Link)
            TaggedItem.objects.filter(content_type=ctype).delete()

        if limit is not None:
            links = (link for link in links[:limit])
        else:
            links = links

        for link in links:
            url = link['href']
            tags = link['tags']
            try:
                Link(url = url, tags = tags).save()
            except Exception:
                logging.exception("can't add link %r with tags %r" % (url, tags))

