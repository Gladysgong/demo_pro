from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=32, unique=True)
    parent = models.ForeignKey("Menu", null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '-'.join(title_list)


class Permission(models.Model):
    title = models.CharField(max_length=32, unique=True)
    url = models.CharField(max_length=128, unique=True)
    menu = models.ForeignKey("Menu", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{menu}---{permission}'.format(menu=self.menu, permission=self.title)


class Role(models.Model):
    title = models.CharField(max_length=32, unique=True)

    permissions = models.ManyToManyField("Permission")

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    username = models.CharField(max_length=32, unique=True)
    # password = models.CharField(max_length=64)
    # nickname = models.CharField(max_length=32)
    # email = models.EmailField()

    roles = models.ManyToManyField("Role")


    def __str__(self):
        return self.nickname


