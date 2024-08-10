from django.db import models
from django.utils import timezone


class Sickbay(models.Model):
    SICKBAY_STATUS = (
        ('occupied', 'Occupied'),
        ('free', 'Free'),
    )

    sickbay_number = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=10, choices=SICKBAY_STATUS, default='free')
    capacity = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    current_occupancy = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return f'Sickbay {self.sickbay_number} ({self.get_status_display()})'

    def is_full(self):
        return self.current_occupancy >= self.capacity

    def update_status(self):
        if self.is_full():
            self.status = 'occupied'
        else:
            self.status = 'free'
        self.save()

    def save(self, *args, **kwargs):
        if self.capacity < 0:
            raise ValueError("Capacity cannot be negative")
        super().save(*args, **kwargs)


class Room(models.Model):
    ROOM_STATUS = (
        ('occupied', 'Occupied'),
        ('free', 'Free'),
    )
    
    ROOM_TYPE = (
        ('private', 'Private'),
        ('icu', 'ICU'),
        ('general', 'General'),
    )

    room_number = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=10, choices=ROOM_STATUS, default='free')
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE)
    capacity = models.IntegerField(default=0)
    current_occupancy = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return f'Room {self.room_number} ({self.get_status_display()})'

    def is_full(self):
        return self.current_occupancy >= self.capacity

    def update_status(self):
        if self.is_full():
            self.status = 'occupied'
        else:
            self.status = 'free'
        self.save()

    def save(self, *args, **kwargs):
        if self.capacity < 0:
            raise ValueError("Capacity cannot be negative")
        super().save(*args, **kwargs)
       
        
class Allocation(models.Model):
    ALLOCATION_TYPE = (
        ('room', 'Room'),
        ('sickbay', 'Sickbay'),
    )

    patient = models.ForeignKey("accounts.Patient", on_delete=models.CASCADE)
    allocation_type = models.CharField(max_length=10, choices=ALLOCATION_TYPE)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
    sickbay = models.ForeignKey(Sickbay, null=True, blank=True, on_delete=models.SET_NULL)
    date_allocated = models.DateTimeField(auto_now_add=True)
    date_released = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.allocation_type == 'room' and self.room:
            self.room.current_occupancy += 1
            self.room.update_status()
            self.room.save()
        elif self.allocation_type == 'sickbay' and self.sickbay:
            self.sickbay.current_occupancy += 1
            self.sickbay.update_status()
            self.sickbay.save()
        elif not self.room and not self.sickbay:
            raise ValueError("Either a room or a sickbay must be allocated")
        super().save(*args, **kwargs)

    def release(self):
        if self.allocation_type == 'room' and self.room:
            self.room.current_occupancy -= 1
            self.room.update_status()
            self.room.save()
        elif self.allocation_type == 'sickbay' and self.sickbay:
            self.sickbay.current_occupancy -= 1
            self.sickbay.update_status()
            self.sickbay.save()
        self.date_released = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.patient} allocated to {self.get_allocation_type_display()}'


class Supplier(models.Model): 
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    
    def __str__(self): 
        return self.name


class Inventory(models.Model):
    ITEM_TYPE_CHOICES = [
        ('Pharmacy', 'Pharmacy'),    
        ('Laboratory', 'Laboratory'),    
        ('Other', 'Other')    
    ]
    
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=50, choices=ITEM_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def update_quantity(self, quantity_change):
        new_quantity = self.quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.quantity = new_quantity
        self.save()

    def save(self, *args, **kwargs):
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        super().save(*args, **kwargs)
