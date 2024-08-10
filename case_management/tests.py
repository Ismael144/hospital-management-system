from django.test import TestCase
from django.utils import timezone
from .models import Case, CaseNote, CarePlan
from accounts.models import Patient, CaseManager  # Assuming these models exist
from django.contrib.auth import get_user_model

User = get_user_model()

class CaseModelTest(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(name='Jane Doe', age=25)  # Assuming Patient has these fields
        self.case_manager = CaseManager.objects.create(name='Manager Name')  # Assuming CaseManager has this field
        self.case = Case.objects.create(
            patient=self.patient,
            case_manager=self.case_manager,
            case_number='CASE123',
        )

    def test_case_str(self):
        self.assertEqual(str(self.case), f"Case CASE123 - {self.patient}")

    def test_case_close_case(self):
        self.case.close_case()
        self.assertEqual(self.case.status, 'Closed')

    def test_case_default_status(self):
        self.assertEqual(self.case.status, 'Open')


class CaseNoteModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='johndoe12@example.com',
            password='password123'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            address='123 Main St',
            phone_number='1234567890',
            date_of_birth='1990-01-01',
            medical_history='No major illnesses',
            status='New Patient'
        )
        self.case_manager = CaseManager.objects.create(name='Some name here')
        self.user = User.objects.create_user(email='someemail@gmail.ug', password='password')
        self.case = Case.objects.create(
            patient=self.patient,
            case_manager=self.case_manager,
            case_number='CASE123',
        )
        self.case_note = CaseNote.objects.create(
            case=self.case,
            author=self.user,
            content='This is a case note.',
        )

    def test_case_note_str(self):
        self.assertEqual(str(self.case_note), f"Note for {self.case}")

    def test_case_note_content(self):
        self.assertEqual(self.case_note.content, 'This is a case note.')

    def test_case_note_date_added(self):
        self.assertIsNotNone(self.case_note.date_added)


class CarePlanModelTest(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(name='Jane Doe', age=25)
        self.case_manager = CaseManager.objects.create(name='Manager Name')
        self.case = Case.objects.create(
            patient=self.patient,
            case_manager=self.case_manager,
            case_number='CASE123',
        )
        self.care_plan = CarePlan.objects.create(
            case=self.case,
            plan_details='Care plan details',
            start_date=timezone.now().date(),
        )

    def test_care_plan_str(self):
        self.assertEqual(str(self.care_plan), f"Care Plan for {self.case.patient}")

    def test_care_plan_status(self):
        self.assertEqual(self.care_plan.status, 'Active')

    def test_care_plan_details(self):
        self.assertEqual(self.care_plan.plan_details, 'Care plan details')

    def test_care_plan_dates(self):
        self.assertIsNotNone(self.care_plan.start_date)
        self.assertIsNone(self.care_plan.end_date)
