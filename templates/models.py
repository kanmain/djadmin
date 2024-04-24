from django.db import models

'''
Xmodel
'''
class Xmodel(models.Model):
  name = models.CharField(max_length=100)
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f'{self.name}'
  
  class Meta:
    verbose_name = 'Xmodel'
    db_table = 'x_xmodel'
    ordering = ('-created_at', )