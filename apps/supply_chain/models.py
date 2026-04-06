from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class SupplyChainEvent(models.Model):
    class EventType(models.TextChoices):
        MANUFACTURED = 'manufactured', _('Manufactured')
        SHIPPED = 'shipped', _('Shipped')
        RECEIVED = 'received', _('Received')
        DISTRIBUTED = 'distributed', _('Distributed')
        SOLD = 'sold', _('Sold')
        RETURNED = 'returned', _('Returned')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(
        'drugs.BatchNumber',
        on_delete=models.CASCADE,
        related_name='supply_chain_events'
    )
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    actor = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='supply_chain_events'
    )
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'supply_chain_events'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.event_type} - {self.batch} at {self.timestamp}'
