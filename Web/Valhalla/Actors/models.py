from django.db import models


class HistoryVikings(models.Model):
    id = models.AutoField(primary_key=True)
    main_url = models.TextField(blank=True, null=True)
    href = models.TextField(blank=True, null=True)
    img_url = models.TextField(blank=True, null=True)
    hero_name = models.TextField(blank=True, null=True)
    actor_name = models.TextField(blank=True, null=True)
    article = models.TextField(blank=True, null=True)
    image_bytes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HISTORY_VIKINGS'


class Norsemen(models.Model):
    href = models.TextField(blank=True, null=True)
    main_url = models.TextField(blank=True, null=True)
    actor_name = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    mini_bio = models.TextField(blank=True, null=True)
    add = models.TextField(blank=True, null=True)
    href_img = models.TextField(blank=True, null=True)
    image_bytes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'NORSEMEN'


class Search(models.Model):
    query = models.CharField(max_length=255)

    def __str__(self):
        return self.query



