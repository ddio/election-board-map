from django.contrib.gis.db import models
from candidates.models import Terms

# 只是想要抓資料，不求完美描述原本的結構

class Boards(models.Model):
    image = models.CharField(max_length=256)
    coordinates = models.PointField()
    took_at = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(null=True)
    uploaded_by = models.UUIDField()
    county = models.CharField(max_length=15)
    district = models.CharField(max_length=15)
    road = models.CharField(max_length=75)
    verified_amount = models.IntegerField()
    is_board = models.BooleanField()
    price = models.IntegerField(null=True, blank=True)
    receipt = models.CharField(max_length=256)
    not_board_amount = models.IntegerField()
    note = models.CharField(max_length=512)
    candidates = models.ManyToManyField(Terms)

class Checks(models.Model):
    slogan = models.CharField(max_length=128)
    is_board = models.BooleanField(null=True, blank=True)
    created_by = models.UUIDField()
    board_id = models.ForeignKey(Boards, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()
    type = models.IntegerField()
    headcount = models.IntegerField()
    is_original = models.BooleanField()
    candidates = models.ManyToManyField(Terms)
