from django.test import TestCase
from django.db import models
from tagging.fields import TagField

class Post(models.Model):
    tags = TagField()

class Link(models.Model):
    tags = TagField()

class TagCloudTests(TestCase):
    def testCreatePost(self):
        self.assertEqual(0, Post.objects.count())
        Post(tags = 'one, two, three').save()
        self.assertEqual(1, Post.objects.count())
