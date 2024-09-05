from django.db import models

# Create your models here.

# User Model
class User(models.Model):
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128)
    profile = models.JSONField(default=dict, null=False)
    status = models.IntegerField(default=0)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.BigIntegerField(null=True)
    updated_at = models.BigIntegerField(null=True)

    def __str__(self):
        return self.email

# Organization Model
class Organization(models.Model):
    name = models.CharField(max_length=255, null=False)
    status = models.IntegerField(default=0, null=False)
    personal = models.BooleanField(default=False, null=True)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.BigIntegerField(null=True)
    updated_at = models.BigIntegerField(null=True)

# Role Model
class Role(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)

# Member Model
class Member(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.BigIntegerField(null=True)
    updated_at = models.BigIntegerField(null=True)
