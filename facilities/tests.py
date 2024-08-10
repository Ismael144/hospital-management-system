from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Sickbay, Room, Allocation, Supplier, Inventory
from accounts.models import Patient
from django.utils import timezone

User = get_user_model()

class SickbayModelTest(TestCase):

    def setUp(self):
        self.sickbay = Sickbay.objects.create(
            sickbay_number='SB001',
            capacity=2,
        )

    def test_sickbay_str(self):
        self.assertEqual(str(self.sickbay), 'Sickbay SB001 (Free)')

    def test_sickbay_is_full(self):
        self.sickbay.current_occupancy = 2
        self.assertTrue(self.sickbay.is_full())

    def test_sickbay_update_status(self):
        self.sickbay.current_occupancy = 2
        self.sickbay.update_status()
        self.assertEqual(self.sickbay.status, 'occupied')

    def test_negative_capacity_raises_error(self):
        with self.assertRaises(ValueError):
            Sickbay.objects.create(sickbay_number='SB002', capacity=-1)


class RoomModelTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(
            room_number='R001',
            room_type='private',
            capacity=1,
        )

    def test_room_str(self):
        self.assertEqual(str(self.room), 'Room R001 (Free)')

    def test_room_is_full(self):
        self.room.current_occupancy = 1
        self.assertTrue(self.room.is_full())

    def test_room_update_status(self):
        self.room.current_occupancy = 1
        self.room.update_status()
        self.assertEqual(self.room.status, 'occupied')

    def test_negative_capacity_raises_error(self):
        with self.assertRaises(ValueError):
            Room.objects.create(room_number='R002', room_type='icu', capacity=-1)


class AllocationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='johndoe@example.com',
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
        self.room = Room.objects.create(room_number='R001', room_type='private', capacity=1)
        self.sickbay = Sickbay.objects.create(sickbay_number='SB001', capacity=2)

    def test_allocation_to_room(self):
        allocation = Allocation.objects.create(patient=self.patient, allocation_type='room', room=self.room)
        self.assertEqual(allocation.room.current_occupancy, 1)

    def test_allocation_to_sickbay(self):
        allocation = Allocation.objects.create(patient=self.patient, allocation_type='sickbay', sickbay=self.sickbay)
        self.assertEqual(allocation.sickbay.current_occupancy, 1)

    def test_allocation_without_room_or_sickbay_raises_error(self):
        with self.assertRaises(ValueError):
            Allocation.objects.create(patient=self.patient, allocation_type='room')

    def test_release_allocation(self):
        allocation = Allocation.objects.create(patient=self.patient, allocation_type='room', room=self.room)
        allocation.release()
        self.assertEqual(allocation.room.current_occupancy, 0)
        self.assertIsNotNone(allocation.date_released)


class SupplierModelTest(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(name='Supplier1', description='Description', location='Location')

    def test_supplier_str(self):
        self.assertEqual(str(self.supplier), 'Supplier1')


class InventoryModelTest(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(name='Supplier1', description='Description', location='Location')
        self.inventory = Inventory.objects.create(
            name='Item1',
            item_type='Pharmacy',
            quantity=10,
            supplier=self.supplier,
        )

    def test_inventory_str(self):
        self.assertEqual(str(self.inventory), 'Item1')

    def test_inventory_update_quantity(self):
        self.inventory.update_quantity(-5)
        self.assertEqual(self.inventory.quantity, 5)

    def test_inventory_update_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.inventory.update_quantity(-20)

    def test_negative_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            Inventory.objects.create(name='Item2', item_type='Laboratory', quantity=-5, supplier=self.supplier)
