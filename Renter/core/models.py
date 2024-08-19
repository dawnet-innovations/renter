from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=100)


class Renter(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='%(class)s_building')
    name = models.CharField(max_length=100)
    agreement_start = models.DateTimeField()
    agreememt_end = models.DateTimeField()
    advance = models.DecimalField(max_digits=10, decimal_places=5)


class Rent(models.Model):
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='%(class)s_renter')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=5)
    balance_paid = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    date = models.DateTimeField()



