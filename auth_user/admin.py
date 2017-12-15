from django.contrib import admin
from auth_user.models import MyUser, MyFriends



# Now register the new UserAdmin...
class MyUserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'person_id', 'is_active', 'is_superuser')

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(MyFriends)





