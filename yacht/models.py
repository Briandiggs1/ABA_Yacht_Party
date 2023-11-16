from django.db import models
import re, bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name must be at least 2 characters long"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be at least 2 characters long."
        if len(postData['email']) < 1:
            errors["email"] = "Email address cannot be blank."
        if len(postData['password']) < 3:
            errors["password"] = "password should be at least 3 characters"
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Please enter a valid email address."
        elif check:
            errors['reg_email'] = "Email address is already registered."
        return errors

    def edit_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 1:
            errors["first_name"] = "First name can not be empty"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Last name can not be empty"
        if len(postData['email']) < 1:
            errors["email"] = "Email address can not be empty"
        return errors
  
    def login_validator(self, postData):
        errors = {}
        # Needs bcrypt to check the user input with the stored hashed password
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password.encode()):
                errors['login_password'] = "Email and password do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class PostManager(models.Manager):
    def simple_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['status']) < 1:
            errors["status"] = "A status must consist of at least 1 character!"
        return errors

class Post(models.Model):
    status = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="writer", on_delete=models.CASCADE)
    liked = models.ManyToManyField(User, related_name="liked_posts")
    #same thing as granted_wish
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()
    