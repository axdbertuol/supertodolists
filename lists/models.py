from django.db import models

# Create your models here.

class List(models.Model):
	pass

class Item(models.Model):
	text = models.TextField(blank=True)
	list = models.ForeignKey(List, blank=True, null=True, on_delete=models.CASCADE)

