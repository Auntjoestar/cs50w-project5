from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class User(AbstractUser):
    def __str__(self):
        return self.username

    pass


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", verbose_name="User's profile",  on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biography")
    PRONOUNS_CHOICES = [
        ("HH", "He/Him"),
        ("SS", "She/Her"),
        ("TT", "They/Them"),
        ("HT", "He/They"),
        ("ST", "She/They"),
        ("IR", "I rather not to say"),
        ("OT", "Other"),
    ]
    pronouns = models.CharField(
        max_length=2, choices=PRONOUNS_CHOICES, default="IR", verbose_name="Pronouns"
    )
    birthdate = models.DateField(default=timezone.now ,null=False, blank=False, verbose_name="Birthdate")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.joined = timezone.now()
        self.updated_at = timezone.now()
        return super(Profile, self).save()

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def serialize(self):
        return {
            "user": self.user.username,
            "name": self.user.first_name,
            "last_name": self.user.last_name,
            "bio": self.bio,
            "pronouns": [self.pronouns, dict(self.PRONOUNS_CHOICES)[self.pronouns]],
            "birthdate": self.birthdate,
        }


class ProfilePicture(models.Model):
    profile = models.OneToOneField(Profile, related_name="picture", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profilePictures", verbose_name="File", blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ProfilePicture, self).save()

    def __str__(self):
        return f"{self.profile.user.username}'s profile picture is {self.image}"
    


class Character(models.Model):
    user = models.ForeignKey(User, related_name="character", verbose_name="User", on_delete=models.CASCADE)
    name = models.CharField(max_length=70, verbose_name="Character's name", blank=False)
    race = models.CharField(max_length=30, verbose_name="Character's race", blank=False)
    class_name = models.CharField(max_length=30, verbose_name="Character's class", blank=False)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")
    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Character, self).save()
    def __str__(self):
        return f"{self.name} is a {self.class_name} of the {self.race} race"
    
class CharacterPicture(models.Model):
    character = models.OneToOneField(Character, related_name="picture",verbose_name="Character's Picture" , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="characterPictures", verbose_name="File")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")
    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(CharacterPicture, self).save()
    def __str__(self):
        return f"{self.character.name}'s picture is {self.image}"

class CharacterStats(models.Model):
    character = models.ForeignKey(Character, related_name="stats", verbose_name="Stats", on_delete=models.CASCADE)
    HP = models.IntegerField(verbose_name="Hit Points", blank=False, default=1, 
                             validators=[MinValueValidator(1), MaxValueValidator(560)])
    XP = models.IntegerField(verbose_name="Experience Points", blank=False, default=0, 
                             validators=[MinValueValidator(0), MaxValueValidator(355000)])
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")
    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(CharacterStats, self).save()
    #edit when campaign model is ready
    def __str__(self):
        return f"{self.character.name}'s stats are HP: {self.HP} and XP: {self.XP}"
    
class CharacterAbilities(models.Model):
    character = models.OneToOneField(Character, related_name="abilities", verbose_name="Character", on_delete=models.CASCADE)
    STR = models.IntegerField(verbose_name="Strength", blank=False, default=1, 
                             validators=[MinValueValidator(1), MaxValueValidator(20)])
    DEX = models.IntegerField(verbose_name="Dexterity", blank=False, default=1, 
                             validators=[MinValueValidator(1), MaxValueValidator(20)])
    CON = models.IntegerField(verbose_name="Constitution", blank=False, default=1, 
                             validators=[MinValueValidator(1), MaxValueValidator(20)])
    INT = models.IntegerField(verbose_name="Intelligence", blank=False, default=1, 
                             validators=[MinValueValidator(1), MaxValueValidator(20)])
    WIS = models.IntegerField(verbose_name="Wisdom", blank=False, default=1, 
                             validators=[MinValueValidator(1), MaxValueValidator(20)])
    CHA = models.IntegerField(verbose_name="Charisma", blank=False, default=1, 
                             validators=[MinValueValidator(1), MaxValueValidator(20)])
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")
    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(CharacterAbilities, self).save()
    def __str__(self):
        return f"{self.character.name}'s abilities are STR: {self.STR}, DEX: {self.DEX}, CON: {self.CON}, INT: {self.INT}, WIS: {self.WIS}, CHA: {self.CHA}"
    
class CharacterInfo(models.Model):
    character = models.OneToOneField(Character, related_name="info", verbose_name="Character", on_delete=models.CASCADE)
    level = models.IntegerField(verbose_name="Level", blank=False, default=1, 
                             validators=[MinValueValidator(1), MaxValueValidator(20)])
    background = models.TextField(max_length=20, verbose_name="Background", blank=True)
    alignment = models.CharField(max_length=30, verbose_name="Alignment", blank=False)
    personality_traits = models.TextField(max_length=100, verbose_name="Personality traits", blank=True)
    ideals = models.TextField(max_length=100, verbose_name="Ideals", blank=True)
    bonds = models.TextField(max_length=250, verbose_name="Bonds", blank=True)
    flaws = models.TextField(max_length=100, verbose_name="Flaws", blank=True)
    about = models.TextField(max_length=500, verbose_name="About", blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")
    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(CharacterInfo, self).save()
    def __str__(self):
        return f"{self.character.name}'s level is {self.level} and alignment is {self.alignment}"
    
class Campaign(models.Model):
    DM = models.ForeignKey(User, related_name="DM", verbose_name="Dungeon Master", on_delete=models.CASCADE)
    name = models.CharField(max_length=70, verbose_name="Campaign's name", blank=False)
    description = models.TextField(max_length=500, verbose_name="Description", blank=True)
    players = models.ManyToManyField(User, related_name="players", verbose_name="Players", blank=True)
    characters = models.ManyToManyField(Character, related_name="characters", verbose_name="Characters", blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")
    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Campaign, self).save()
    def __str__(self):
        return f"{self.name} is a campaign created by {self.DM.username}"

class CampaignPicture(models.Model):
    campaign = models.OneToOneField(Campaign, related_name="picture", verbose_name="Campaign's picture", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="campaignPictures", verbose_name="File")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")
    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(CampaignPicture, self).save()
    def __str__(self):
        return f"{self.campaign.name}'s picture is {self.image}"
    
class CampaignMap(models.Model):
    campaign = models.OneToOneField(Campaign, related_name="map", verbose_name="Campaign's map", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="campaignMaps", verbose_name="File")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")
    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(CampaignMap, self).save()
    def __str__(self):
        return f"{self.campaign.name}'s map is {self.image}"
    
class Movements(models.Model):
    character = models.ForeignKey(Character, related_name="movements", verbose_name="Character", on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, related_name="movements", verbose_name="Campaign", on_delete=models.CASCADE)
    feets = models.IntegerField(verbose_name="Feets", blank=False, default=0, 
                             validators=[MinValueValidator(0), MaxValueValidator(253440)])
    y_position = models.IntegerField(verbose_name="Y Position", blank=False, default=0)
    x_position = models.IntegerField(verbose_name="X Position", blank=False, default=0)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")
    def save(self):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Movements, self).save()
    def __str__(self):
        return f"{self.character.name} is moving in {self.campaign.name}"
    
class Action(models.Model):
    campaign = models.ForeignKey(Campaign, related_name="actions", verbose_name="Campaign", on_delete=models.CASCADE)
    character = models.ForeignKey(Character, related_name="actions", verbose_name="Character", on_delete=models.CASCADE)
    description = models.TextField(max_length=500, verbose_name="Description", blank=True)
    action_type = models.CharField(max_length=30, verbose_name="Type", blank=False)
    target = models.CharField(max_length=70, verbose_name="Target", blank=True)
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Timestamp")

class Reaction(models.Model):
    campaign = models.ForeignKey(Campaign, related_name="reactions", verbose_name="Campaign", on_delete=models.CASCADE)
    character = models.ForeignKey(Character, related_name="reactions", verbose_name="Character", on_delete=models.CASCADE)
    description = models.TextField(max_length=500, verbose_name="Description", blank=True)
    reaction_type = models.CharField(max_length=30, verbose_name="Type", blank=False)
    target = models.CharField(max_length=70, verbose_name="Target", blank=True)
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Timestamp")

class CampaignLog(models.Model):
    campaign = models.ForeignKey(Campaign, related_name="log", verbose_name="Campaign", on_delete=models.CASCADE)
    character = models.ManyToManyField(Character, related_name="log", verbose_name="Character")
    description = models.TextField(max_length=500, verbose_name="Description", blank=True)
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Timestamp")