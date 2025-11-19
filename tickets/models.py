from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField( blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tickets')
    created_by= models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_tickets')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('cancelled', 'Cancelled'),
        ('closed', 'Closed'),
    ], default='open')

    def __str__(self):
        return self.title