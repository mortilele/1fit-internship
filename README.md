# 1Fit Internship Task

## Implementation description:

## Local setup manual:
### Admin access
```python
from internship.core.models import CustomUser
from datetime import date
CustomUser.objects.create_superuser('admin', 'admin@1fit.app', 'admin', birth_date=date(1999, 9, 11))
```