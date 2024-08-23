from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Renter(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='%(class)s_building')
    room = models.CharField(max_length=25)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    whatsapp = models.CharField(max_length=15, null=True, blank=True)
    agreement_start = models.DateTimeField()
    agreement_end = models.DateTimeField()
    advance = models.DecimalField(max_digits=10, decimal_places=5)
    rent = models.DecimalField(max_digits=10, decimal_places=5)

    def save(self, *args, **kwargs):
        if not self.whatsapp:
            self.whatsapp = self.phone
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Rent(models.Model):
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='%(class)s_renter')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=5)
    balance = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def is_paid(self):
        return self.balance == 0

    def __str__(self):
        return self.renter.name



