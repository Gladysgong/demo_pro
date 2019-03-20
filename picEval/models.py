from django.db import models
# from rbac.models import UserInfo


# Create your models here.
class ImageTaskInfo(models.Model):
    id = models.AutoField(primary_key=True)
    # username = models.ForeignKey(to=UserInfo, to_field='username', on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    env_type = models.IntegerField(default=0)

    start_time = models.CharField(max_length=50, default="")
    end_time = models.CharField(max_length=50, default="")

    testtag = models.CharField(max_length=50, default="")
    errorlog = models.TextField(default="")
    pid = models.CharField(max_length=50, default="")

    test_ocrip = models.CharField(max_length=50, default="")
    base_ocrip = models.CharField(max_length=50, default="")
    test_imgip = models.CharField(max_length=50, default="")
    base_imgip = models.CharField(max_length=50, default="")

    sum_num = models.IntegerField(default=0)
    finished = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)
    img_diff_count = models.IntegerField(default=0)
    text_diff_count = models.IntegerField(default=0)
    text_base_count = models.IntegerField(default=0)

    path=models.CharField(max_length=500,default="")

    langs = models.CharField(max_length=50, default="")

    svIP = models.CharField(max_length=50, default="")
    svUser = models.CharField(max_length=100, default="")
    svPass = models.CharField(max_length=100, default="")
    svPath = models.CharField(max_length=1000, default="")

    sourceIP = models.CharField(max_length=50, default="")
    sourceUser = models.CharField(max_length=100, default="")
    sourcePass = models.CharField(max_length=100, default="")
    sourcePath = models.CharField(max_length=500, default="")


class ResultInfo(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=500, default="")
    testImg = models.CharField(max_length=500, default="")
    basepath = models.CharField(max_length=500, default="")
    testpath = models.CharField(max_length=500, default="")
    taskid = models.ForeignKey(to="ImageTaskInfo", to_field='id', on_delete=models.CASCADE)
    result = models.TextField()
    rankInfo = models.IntegerField(default=0)
    test_status = models.IntegerField(default=0)
    base_status = models.IntegerField(default=0)
