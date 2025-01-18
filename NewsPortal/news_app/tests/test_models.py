import unittest

from news_app.models import Category, Post


class CategoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.categories = Category.objects.all()
        cls.category = cls.categories.last()

    def test_category_max_length(self):
        max_length = self.category._meta.get_field('category').max_length
        self.assertEqual(max_length, 64)

    def test_category_str(self):
        expected_str = self.category.category
        self.assertEqual(expected_str, str(self.category))


class PostTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.posts = Post.objects.all()
        cls.post = cls.posts.last()

    def test_like_dislike(self):
        before_like = self.post.rating
        self.post.like()
        self.assertEqual(self.post.rating, before_like + 1)
        self.post.dislike()
        self.assertEqual(self.post.rating, before_like)

