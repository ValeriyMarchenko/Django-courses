from django.db import models
from django.contrib.auth.models import User

class Advert(models.Model):
    CATEGORY = [
        ('Tanks', 'Tanks'),
        ('Healers', 'Healers'),
        ('DDs', 'DDs'),
        ('Traders', 'Traders'),
        ('GildMasters', 'GildMasters'),
        ('QuestGivers', 'QuestGivers'),
        ('Smiths', 'Smiths'),
        ('Tanners', 'Tanners'),
        ('Potions', 'Potions'),
        ('SpellMasters', 'SpellMasters')
    ]

    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_category = models.CharField(max_length=12, choices=CATEGORY, default='DDs')
    text = models.TextField()
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        string = self.text[0:20]
        if len(self.text) > len(string):
            string += "..."
        return string


class Response(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    text = models.TextField()
    accepted = models.BooleanField(default=False)