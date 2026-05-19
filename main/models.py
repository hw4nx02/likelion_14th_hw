from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

class Post(models.Model):
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, verbose_name='post_image')
    pub_date = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    like = models.ManyToManyField(User, related_name="post_likes", blank=True)
    like_count = models.PositiveIntegerField(default=0)

    # 20자 넘으면 ... 붙이고 요약
    def summary(self):
        str = self.content
        if len(self.content) > 20:
            str = str[:20] + "..."
        return str
    
class Comment(models.Model):
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name="comment_likes", blank=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.post.title}: {self.post.content[:20]} by {self.writer.profile.nickname}"