from nose.tools import eq_

import amo.tests
from mkt.ratings.models import check_spam, Review, Spam
from mkt.site.fixtures import fixture
from mkt.webapps.models import Webapp
from users.models import UserProfile


class TestSpamTest(amo.tests.TestCase):
    fixtures = fixture('webapp_337141')

    def setUp(self):
        self.app = Webapp.objects.get(pk=337141)
        self.user = UserProfile.objects.get(pk=31337)
        Review.objects.create(addon=self.app, user=self.user, title="review 1")
        Review.objects.create(addon=self.app, user=self.user, title="review 2")

    def test_create_not_there(self):
        Review.objects.all().delete()
        eq_(Review.objects.count(), 0)
        check_spam(1)

    def test_add(self):
        assert Spam().add(Review.objects.all()[0], 'numbers')