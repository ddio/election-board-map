from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

# 只是想要抓資料，不求完美描述原本的結構

class Candidates(models.Model):
    uid = models.UUIDField(unique=True)
    name = models.CharField(max_length=100)
    birth = models.DateField(null=True, blank=True)
    former_names = models.CharField(max_length=100)
    identifiers = JSONField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

class Terms(models.Model):
    uid = models.CharField(max_length=70, unique=True)
    councilor_terms = JSONField(null=True, blank=True)
    election_year = models.CharField(max_length=100)
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, null=True)
    party = models.CharField(max_length=100, null=True)
    constituency = models.IntegerField()
    county = models.CharField(max_length=100)
    district = models.TextField()
    votes = models.IntegerField()
    votes_percentage = models.CharField(max_length=100)
    elected = models.BooleanField()
    contact_details = JSONField()
    education = models.TextField()
    experience = models.TextField()
    remark = models.TextField()
    image = models.CharField(max_length=200)
    links = JSONField()
    platform = models.TextField()
    politicalcontributions = JSONField()
    candidate = models.ForeignKey(Candidates, on_delete=models.DO_NOTHING, to_field='uid')
    elected_councilor_id = models.IntegerField()
    data = JSONField()
    type = models.CharField(max_length=20)
    votes_detail = JSONField()
    occupy = models.BooleanField()
    status = models.CharField(max_length=100)
