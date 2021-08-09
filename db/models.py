import sys, os

# sys.path.append('/Users/joeychun/Desktop/Pythons/Django-ORM-test/Django-ORM/main2.py')
# from '/Users/joeychun/Desktop/Pythons/Django-ORM-test/Django-ORM/main2.py' import Summoner
# from '../main2.py' import Summoner
# import importlib.util

# spec = importlib.util.spec_from_file_location("main2", "/Users/joeychun/Desktop/Pythons/Django-ORM-test/Django-ORM/main2.py")
# maincode = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(maincode)

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()


class DBUser(models.Model):
    discordServer = models.BigIntegerField()
    summonerName = models.CharField(max_length=100)
    summonerId = models.CharField(max_length=100)
    summonerLevel = models.IntegerField()
    region = models.CharField(max_length=100)
    discordUser = models.BigIntegerField(default=-1)

    def __str__(self):
        return self.summonerName
    
    def returnSummonerInfo(self):
        return [self.summonerName, self.summonerId, self.summonerLevel, self.region]

