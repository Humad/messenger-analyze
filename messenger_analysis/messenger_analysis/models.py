from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('id',)

class BlockedWord(models.Model):
    word = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ('word',)
