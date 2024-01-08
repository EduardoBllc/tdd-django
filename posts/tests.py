from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from posts.models import Post
from http import HTTPStatus
from model_bakery import baker


class PostModelTest(TestCase):
    def test_post_model_exist(self):
        post = Post.objects.count()

        self.assertEqual(post, 0)

    def test_string_rep_of_objects(self):
        post = baker.make(Post)
        self.assertEqual(str(post), post.title)
        self.assertTrue(isinstance(post, Post))


class HomePageTest(TestCase):
    def setUp(self) -> None:
        self.post1 = baker.make(Post)
        self.post2 = baker.make(Post)

    def test_homepage_returns_correct_response(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'posts/index.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_returns_list_view(self):
        response = self.client.get('/')
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)


class DetailPageTest(TestCase):
    def setUp(self) -> None:
        self.post = baker.make(Post)

    def test_detail_page_returns_correct_response(self):
        response = self.client.get(self.post.get_absolute_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/detail.html')

    def test_detail_test_returns_correct_context(self):
        response = self.client.get(self.post.get_absolute_url())

        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)


class PostAuthorTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)
        self.post = Post.objects.create(
            title="Test title",
            body="Test body",
            author=self.user
        )

    def test_author_is_instance_of_user_model(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertTrue(isinstance(self.post, Post))

    def test_post_belongs_to_user(self):
        self.assertTrue(hasattr(self.post, 'author'))
        self.assertTrue(self.post.author, self.user)
