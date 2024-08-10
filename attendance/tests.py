from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Attendance

User = get_user_model()

class AttendanceModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe', 
            email='johndoe@example.com', 
            password='password123'
        )
        self.attendance = Attendance.objects.create(
            user=self.user,
            role='doctor',
            date=timezone.now().date(),
            time_in=timezone.now().time(),
        )

    def test_attendance_str(self):
        self.assertEqual(str(self.attendance), f'{self.user.email} - {self.attendance.date} - {self.attendance.get_status_display()}')

    def test_attendance_default_status(self):
        self.assertEqual(self.attendance.status, 'present')

    def test_attendance_role_choices(self):
        self.assertIn(self.attendance.role, dict(Attendance.ROLE_CHOICES).keys())

    def test_attendance_time_in(self):
        self.assertIsNotNone(self.attendance.time_in)

    def test_attendance_time_out_default(self):
        self.assertIsNone(self.attendance.time_out)

    def test_attendance_update_time_out(self):
        new_time_out = timezone.now().time()
        self.attendance.time_out = new_time_out
        self.attendance.save()
        self.assertEqual(self.attendance.time_out, new_time_out)

    def test_attendance_status_choices(self):
        self.assertIn(self.attendance.status, dict(Attendance.STATUS_CHOICES).keys())
