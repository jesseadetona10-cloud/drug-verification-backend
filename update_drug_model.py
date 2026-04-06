with open('apps/drugs/models.py', 'r') as f:
    content = f.read()
content = content.replace(
    'ACTIVE = "active", _("Active")\n        RECALLED = "recalled", _("Recalled")\n        EXPIRED = "expired", _("Expired")\n        SUSPENDED = "suspended", _("Suspended")',
    'PENDING = "pending", _("Pending Approval")\n        ACTIVE = "active", _("Active")\n        REJECTED = "rejected", _("Rejected")\n        RECALLED = "recalled", _("Recalled")\n        EXPIRED = "expired", _("Expired")\n        SUSPENDED = "suspended", _("Suspended")'
)
content = content.replace(
    'default=Status.ACTIVE)',
    'default=Status.PENDING)'
)
with open('apps/drugs/models.py', 'w') as f:
    f.write(content)
print('Done')
