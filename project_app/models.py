from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postdata):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['f_n'])<2:
            errors['f_n']="First Name must be longer than 2 characters!"
        if len(postdata['l_n'])<2:
            errors['l_n']="Last Name must be longer than 2 characters!"
        if not email_check.match(postdata['email']):
            errors['email']="Email must be a valid format!"
        if len(postdata['pw'])<8:
            errors['pw']="Password must be at least 8 characters!"
        if postdata['pw'] != postdata['conf_pw']:
            errors['conf_pw']="Password and confirm password must match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class ForumManager(models.Manager):
    def empty_validator(self, postdata):
        errors=""
        if len(postdata['contents']) < 1:
            errors="You must provide content on your post."
        return errors

class Forum(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    objects = ForumManager()

class Comment(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    message = models.ForeignKey(Forum, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)