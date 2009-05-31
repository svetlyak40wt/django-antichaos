from django.test import TestCase
from django.db import models

from tagging.fields import TagField
from tagging.models import Tag, TaggedItem
from django_antichaos.utils import *


class Post(models.Model):
    title = models.CharField(max_length = 20)
    tags = TagField()

    def __unicode__(self):
        return self.title


class Link(models.Model):
    url = models.CharField(max_length = 20)
    tags = TagField()

    def __unicode__(self):
        return self.url

class TagCloudTests(TestCase):
    def testCreatePost(self):
        self.assertEqual(0, Post.objects.count())
        Post(tags = 'one, two, three').save()
        self.assertEqual(1, Post.objects.count())

    def testContentTypes(self):
        Post(tags = 'one, two, three').save()
        Link(tags = 'six, seven').save()

        mods = [m for ctype_id, m in get_tagged_models()]
        self.assertEqual(2, len(mods))
        self.assert_(Post in mods)
        self.assert_(Link in mods)

class CommandsTests(TestCase):
    def setUp(self):
        self.post_ctype = model_to_ctype(Post)
        self.link_ctype = model_to_ctype(Link)

        self.post1 = Post(title = 'First post', tags = 'one, two, three')
        self.post1.save()
        Post(title = 'Second post', tags = 'five, six').save()

        Link(url = 'http://blah.com', tags = 'five, seven').save()
        Link(url = 'http://minor.com', tags = 'two, three').save()

        self.tagids = dict((tag.name, tag.id) for tag in Tag.objects.all())

    def testMerge(self):
        self.assertEqual(1, TaggedItem.objects.get_by_model(Post, 'two').count())
        self.assertEqual(1, TaggedItem.objects.get_by_model(Post, 'five').count())
        self.assertEqual(1, TaggedItem.objects.get_by_model(Link, 'three').count())
        self.assertEqual(1, TaggedItem.objects.get_by_model(Link, 'five').count())
        self.assertEqual('one three two', Post.objects.get(id=self.post1.id).tags)

        t = self.tagids
        process_commands(self.post_ctype, [
            'merge|%s|%s' % (t['three'], t['five']),
            'merge|%s|%s' % (t['two'], t['three']),
        ])

        self.assertEqual(2, TaggedItem.objects.get_by_model(Post, 'two').count())
        self.assertEqual(0, TaggedItem.objects.get_by_model(Post, 'five').count())
        self.assertEqual(1, TaggedItem.objects.get_by_model(Link, 'three').count())
        self.assertEqual(1, TaggedItem.objects.get_by_model(Link, 'five').count())
        self.assertEqual('one two', Post.objects.get(id=self.post1.id).tags)

    def testRename(self):
        self.assertEqual(1, TaggedItem.objects.get_by_model(Post, 'five').count())
        self.assertEqual(1, TaggedItem.objects.get_by_model(Link, 'five').count())
        self.assertEqual(0, TaggedItem.objects.get_by_model(Post, 'new-tag').count())

        t = self.tagids
        process_commands(self.post_ctype, [
            'rename|%s|%s' % (t['five'], 'new-tag'),
        ])

        self.assertEqual(0, TaggedItem.objects.get_by_model(Post, 'five').count())
        self.assertEqual(1, TaggedItem.objects.get_by_model(Link, 'five').count())
        self.assertEqual(1, TaggedItem.objects.get_by_model(Post, 'new-tag').count())

