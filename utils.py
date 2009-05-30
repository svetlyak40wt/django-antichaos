import logging
from BeautifulSoup import BeautifulSoup
from antichaos_example.models import Link

def upload(filename = '../bookmarks.html'):
    soup = BeautifulSoup(open(filename))
    links = soup.findAll('a', attrs = dict(tags=lambda tag: tag))

    Link.objects.all().delete()

    for link in links:
        url = link['href']
        tags = link['tags']
        try:
            Link(url = url, tags = tags).save()
        except Exception:
            logging.exception("can't add link %r with tags %r" % (url, tags))
