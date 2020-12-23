from django.db import models


class Purchase(models.Model):
    purchaser_name = models.CharField(max_length=50, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = "purchase"
        ordering = ["pk"]

    def __str__(self):
        return f'{self.purchaser_name} | {self.quantity}'


class PurchaseStatus(models.Model):
    status_choices = (
        ('Open', 'Open'),
        ('Verified', 'Verified'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
    )
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=status_choices, default='Open')
    created_at = models.DateTimeField(null=False, blank=False)

    class Meta:
        db_table = "purchase_status"
        ordering = ["pk"]

    def __str__(self):
        return f'{self.purchase} | {self.status} | {self.created_at.strftime("%d-%m-%Y")}'