from datetime import datetime
from django.test import TestCase
from posts.models import Post
from myblog.lor_ips import short_lorips
from http import HTTPStatus


class PostModelTest(TestCase):
    def test_post_model_exist(self):
        posts = Post.objects.count()

        self.assertEqual(posts, 0)

    def test_string_rep_of_objects(self):
        post = Post(
            title="Test Post",
            body="Test body",
            created_at=datetime.now(),
            modified_at=datetime.now(),
        )
        self.assertEqual(str(post), post.title)


class HomePageTest(TestCase):
    def setUp(self) -> None:
        post2 = Post.objects.create(
            title="sample post 1",
            body=short_lorips,
        )

        post1 = Post.objects.create(
            title="sample post 2",
            body=short_lorips,
        )

    def test_homepage_returns_correct_response(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'posts/index.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_returns_list_view(self):
        response = self.client.get('/')
        self.assertContains(response, "sample post 1")
        self.assertContains(response, "sample post 2")


class DetailPageTest(TestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(
            title="sample post 1",
            body=short_lorips,
        )

    def test_detail_page_returns_correct_response(self):
        response = self.client.get(self.post.get_absolute_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/details.html')
