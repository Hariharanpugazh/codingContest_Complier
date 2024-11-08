from djongo import models

class ContestDetails(models.Model):
    contest_name = models.CharField(max_length=100)
    start_time = models.CharField(max_length=50)
    end_time = models.CharField(max_length=50)
    organization_type = models.CharField(max_length=50)
    organization_name = models.CharField(max_length=100)
    testType = models.CharField(max_length=10)

    class Meta:
        db_table = 'Contest_Details'  # MongoDB collection name