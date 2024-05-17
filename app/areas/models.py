from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subs', null=True)

    class Meta:
        db_table = 'tk_areas'
