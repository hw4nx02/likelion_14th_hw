from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=50)
    writer = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, verbose_name='post_image')
    pub_date = models.DateField()

    # 20자 넘으면 ... 붙이고 요약
    def summary(self):
        str = self.content
        if len(self.content) > 20:
            str = str[:20] + "..."
        return str