from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class category(models.Model):
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class expense(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    category=models.CharField(max_length=50)
    amount= models.DecimalField(max_digits=10 , decimal_places=2)
    description= models.TextField()
    date= models. DateField()

    def __str__(self):
        return f"{self.category}- {self. amount}"
    
