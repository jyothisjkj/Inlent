from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Letter(models.Model):
    user = models.ForeignKey(
        "accounts.CustomUser", on_delete=models.CASCADE, related_name="letters"
    )
    # Sender details
    sender_fullname = models.CharField("Full Name", max_length=100, default="")
    sender_nickname = models.CharField(
        "Nick Name", max_length=50, blank=True, null=True, default=""
    )
    sender_place = models.CharField(
        "Place / Address Line 1", max_length=100, default=""
    )
    sender_city = models.CharField("City", max_length=100, default="")
    sender_state = models.CharField("State", max_length=100, default="")
    sender_country = models.CharField("Country", max_length=100, default="India")
    sender_pincode = models.CharField("Pincode", max_length=20, default="")

    # Receiver details
    receiver_fullname = models.CharField(
        "Full Name", max_length=100, null=True, blank=True
    )
    receiver_nickname = models.CharField(
        "Nick Name", max_length=50, blank=True, null=True
    )
    receiver_place = models.CharField(
        "Place / Address Line 1", max_length=100, null=True, blank=True
    )
    receiver_city = models.CharField("City", max_length=100, null=True, blank=True)
    receiver_state = models.CharField("State", max_length=100, null=True, blank=True)
    receiver_country = models.CharField("Country", max_length=100, default="India")
    receiver_pincode = models.CharField("Pincode", max_length=20, null=True, blank=True)

    delivery_date = models.DateField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="letters/images/", null=True, blank=True)
    caption = models.CharField(max_length=300, null=True, blank=True)

    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Letter from {self.sender_fullname} to {self.receiver_fullname} (Delivery: {self.delivery_date})"

    class Meta:
        ordering = ["-delivery_date"]
