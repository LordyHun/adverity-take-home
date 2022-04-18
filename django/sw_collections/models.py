from django.db import models
from django.conf import settings

# Create your models here.
class SWDataCollection(models.Model):
    """
    Base model for a set of collections
    """
    timestamp = models.DateTimeField(auto_created=True, auto_now_add=True)
    data_file = models.FilePathField(path=settings.COLLECTIONS_DIR, null=False)
