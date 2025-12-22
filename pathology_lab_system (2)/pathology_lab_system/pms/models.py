from django.db import models
from django.contrib.auth.models import User

class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='test_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('REPORT_READY', 'Report Ready'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # logged-in user
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')


    # patient info from popup form
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField(blank=True)


    def __str__(self):
        return f"{self.user.username} - {self.test.name} ({self.status})"


class TestReport(models.Model):
    """Stores the result file and links it to a specific booking."""

    # Link to the specific booking
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='report')

    # Field to hold the file (will require setting up media root)
    # The uploaded file (e.g., PDF, JPEG)
    report_file = models.FileField(upload_to='test_reports/')

    # A dummy field to show who uploaded/confirmed it
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for Booking ID {self.booking.id}"