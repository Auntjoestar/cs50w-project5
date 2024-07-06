from django.contrib import admin

# Register your models here.
from .models import (
    User,
    Profile,
    ProfilePicture,
    Character,
    CharacterPicture,
    CharacterStats,
    CharacterInfo,
    Campaign,
    CampaignPicture,
    CampaignMap,
    Movements,
    Action,
    Reaction,
    CampaignLog,
)

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ProfilePicture)
admin.site.register(Character)
admin.site.register(CharacterPicture)
admin.site.register(CharacterStats)
admin.site.register(CharacterInfo)
admin.site.register(Campaign)
admin.site.register(CampaignPicture)
admin.site.register(CampaignMap)
admin.site.register(Movements)
admin.site.register(Action)
admin.site.register(Reaction)
admin.site.register(CampaignLog)
