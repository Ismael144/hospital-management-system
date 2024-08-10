from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Activity

User = get_user_model()

class ActivityModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe', 
            email='johndoe@example.com', 
            password='password123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            action='login',
            description='User logged in successfully.',
        )

    def test_activity_str(self):
        self.assertEqual(
            str(self.activity), 
            f'{self.user} - {self.activity.action} at {self.activity.timestamp}'
        )

    def test_activity_action_choices(self):
        self.assertIn(self.activity.action, dict(Activity.ACTION_CHOICES).keys())

    def test_activity_default_description(self):
        activity_no_description = Activity.objects.create(
            user=self.user,
            action='logout'
        )
        self.assertIsNone(activity_no_description.description)

    def test_activity_timestamp_auto_now_add(self):
        self.assertIsNotNone(self.activity.timestamp)
        self.assertAlmostEqual(self.activity.timestamp, timezone.now(), delta=timezone.timedelta(seconds=1))
