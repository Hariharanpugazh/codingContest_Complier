from django.db import models

# Create your models here.
from djongo import models

class FileUploadProblems(models.Model):
    title = models.CharField(max_length=255)
    level = models.CharField(max_length=50)
    problem_statement = models.TextField()
    sample_input_1 = models.TextField(blank=True, null=True)
    sample_output_1 = models.TextField(blank=True, null=True)
    sample_input_2 = models.TextField(blank=True, null=True)
    sample_output_2 = models.TextField(blank=True, null=True)
    sample_input_3 = models.TextField(blank=True, null=True)
    sample_output_3 = models.TextField(blank=True, null=True)
    sample_input_4 = models.TextField(blank=True, null=True)
    sample_output_4 = models.TextField(blank=True, null=True)
    hidden_input_1 = models.TextField(blank=True, null=True)
    hidden_output_1 = models.TextField(blank=True, null=True)
    hidden_input_2 = models.TextField(blank=True, null=True)
    hidden_output_2 = models.TextField(blank=True, null=True)
    hidden_input_3 = models.TextField(blank=True, null=True)
    hidden_output_3 = models.TextField(blank=True, null=True)
    hidden_input_4 = models.TextField(blank=True, null=True)
    hidden_output_4 = models.TextField(blank=True, null=True)
    hidden_input_5 = models.TextField(blank=True, null=True)
    hidden_output_5 = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'FileUpload'  # MongoDB collection name