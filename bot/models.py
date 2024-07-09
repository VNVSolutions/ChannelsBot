from django.db import models


class MainChannel(models.Model):
    channel_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubChannel(models.Model):
    main_channel = models.ForeignKey(MainChannel, related_name='sub_channels', on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class KeywordReplacement(models.Model):
    sub_channel = models.ForeignKey(SubChannel, related_name='keyword_replacements', on_delete=models.CASCADE)

    def __str__(self):
        return f'Keyword Replacements for {self.sub_channel}'

class KeywordReplacementItem(models.Model):
    keyword_replacement = models.ForeignKey(KeywordReplacement, related_name='items', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    replacement = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.keyword} -> {self.replacement}'
