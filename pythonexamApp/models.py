from django.db import models
import re
from datetime import date

# Create your models here.
class UserManager(models.Manager):
    def registerValidator(self, postData):
        errors = {}
        userMatch = User.objects.filter(username = postData['uname'])
        # EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # add keys and values to errors dictionary for each invalid field
        # first name required
        if len(postData['name']) <=3:
            errors['namereq'] = "Name must be at least 3 characters"
        # username required
        if len(postData['uname']) <=3:
            errors['unamereq'] = "Username must be at least 3 characters"
        if len(userMatch)>0:
            errors['duplicateUser'] = "Username is already taken"
        # email required
        # if len(postData['eMail']) ==0:
        #     errors['eMailreq'] = "Email required"
        # #make sure email is in correct format
        # elif not EMAIL_REGEX.match(postData['eMail']):          
        #     errors['emailpattern'] = "Invalid email address!"
        # password at least 3 chars
        if len(postData['pw']) <3:
            errors['pwreq'] = "Password must at least 3 characters"
        # password and confirm pw must match
        if postData['pw'] != postData['cpw']:
            errors['cpwmatch'] = "Confirm password must match"
        return errors

    def loginValidator(self, postData):
        errors = {}
        # ClassName.objects.filter(field1="value for field1", etc.) - gets any records matching the query provided
        userMatch = User.objects.filter(username = postData['uname'])
        print("PRINTING LIST OF USERS WHO MATCH THE LOGIN PASSWORD FROM LOGIN FORM")
        print(userMatch)
        if len(postData['uname']) ==0:
            errors['unamereq'] = "Username is required"
        elif len(userMatch) == 0:
            errors['usernomatch'] = "Username does not exist"
        else:
            # if we end up here, username exists and is valid
            # check the password
            print ("THAT WAS A VALID USERNAME")
            print (userMatch[0].password)
            if userMatch[0].password != postData['pw']:
                errors['pwmatch'] = "Incorrect Password"

        return errors

class TripManager(models.Manager):
    def tripValidator(self, postData):
        errors = {}
        today = date.today()
        # no empty entries
        if len(postData['dest']) ==0:
            errors['destreq'] = "Destination is required"
        # travel date must be in future
        elif len(postData['dest']) <3:
            errors['destreq'] = "Destination must be at least 3 characters"
        if len(postData['desc']) ==0:
            errors['descreq'] = "Description required"

        if len(postData['fdate']) ==0:
            errors['fdatereq'] = "Departure date required"
        elif postData['fdate'] < str(today):
            errors['datepassed'] = "Date can not be in the past"
        # travel date to must be after travel date from
        if len(postData['tdate']) ==0:
            errors['tdatereq'] = "Return date required"
        elif postData['tdate'] < postData['fdate']:
            errors['latedatereq'] = "Return date must be after departure date"
        
        
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    uploader = models.ForeignKey(User, related_name = "trip_added", on_delete = models.CASCADE)
    joiner = models.ManyToManyField(User, related_name = "trip_joined")
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()