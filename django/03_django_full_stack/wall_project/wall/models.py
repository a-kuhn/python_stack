from django.db import models
from django.contrib import messages
import re
import bcrypt
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, post_data):
        print("*****post_data: ", post_data)
        errors = {}
        #is email already in db?  --> yes = add message to errors, return errors
        potential_new_user = User.objects.filter(email = post_data['email'])
        if len(potential_new_user)>0:
            errors['not_new'] = "Email already registered"
            return errors
        #regex for email, len(first_name, last_name, password, pw==pw_confirm)
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        if len(post_data['first_name'])<2:
            errors['first_name'] = "first name too short"
        if len(post_data['last_name'])<2:
            errors['last_name'] = "last name too short"
        if len(post_data['password'])<6:
            errors['password'] = "password too short"
        if post_data['password'] != post_data['pw_confirm']:
            errors['pw_match'] = "passwords do not match"
        if post_data['dob'] > datetime.now().strftime("%Y-%m-%d"):
            errors['dob'] = "invalid birthdate"
        #check if user is at least 13 yrs old     
        if int(datetime.now().strftime("%Y%m%d")) - int(re.sub('-', '', post_data['dob'])) <=130000:
            errors['dob'] = "sorry, you're too young!" 

        return errors

    def login_validator(self, post_data):
        errors = {}
        #is email in db?  --> no = add message to errors, return erros
        login_attempt = User.objects.filter(email = post_data['email'])
        if len(login_attempt)==0:
            errors['existing_email'] = "This email has not been registered"
            return errors
        #does pw match
        if not bcrypt.checkpw(post_data['password'].encode(), User.objects.filter(email = post_data['email'])[0].password.encode()):
            errors['password'] = "That password doesn't work."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateTimeField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def formatted_dob(self):
        return self.dob.strftime("%Y-%m-%d")

class Message(models.Model):
    m_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    def created_date(self):
        return created_at.strftime('%B %d'+','+' %Y')


class Comment(models.Model):
    c_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    def created_date(self):
        return created_at.strftime('%B %d'+','+' %Y')