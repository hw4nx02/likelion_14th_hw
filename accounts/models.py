from django.contrib.auth.models import User
from django.dispatch import receiver # 신호 기능
from django.db import models
from django.db.models.signals import post_save # 신호 수신 대기
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10)
    age = models.IntegerField(null=True, blank=True)
    major = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name="followers", blank=True)

    def __str__(self):
        return self.nickname
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image:
            image = Image.open(self.profile_image.path)
            max_size = (300, 300)
            image.thumbnail(max_size)
            image.save(self.profile_image.path)

# receiver(수신자 함수, 발신자 객체)
"""
sender - 신호를 보낸 모델
instance - 방금 저장된 모델의 객체
created - 처음 만들어진 거면 True, 수정이면 False
**kwargs - 추가적인 키워드 인자
"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created: # 처음 만들어졌으면
        Profile.objects.create(user=instance) # Profile 자동 생성

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # User 정보 수정 시 Profile도 함께 저장
    instance.profile.save()