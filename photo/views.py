from django.shortcuts import render, redirect
from auth_user.models import MyUser, MyFriends
from photo.models import UserPhoto
from chat.models import Chat

# Create your views here.
def all_friends(user):
	''' функция для отображения всех друзей пользователя. Возвращает множество друзей и их общее количество.'''
	iam_initiator = MyFriends.objects.filter(man=user, status=1) 
	iam_friend = MyFriends.objects.filter(friend=user, status=1)

	my_friends = set()
	for person in iam_initiator:
		my_friends.add(person.friend)
	for person in iam_friend:
		my_friends.add(person.man)
	friends_count = 0
	for i in my_friends:
		friends_count += 1
	return my_friends, friends_count



def person_photo(request, person_id):
	''' функция для отображения страницы с фотоальбомом пользователя'''
	try:
		user = MyUser.objects.get(person_id=person_id)
		#находим все фото пользователя
		all_photos = UserPhoto.objects.filter(user = user)
		photos = []
		pair_photo = []
		i = 1
		#разбиваем фото по парам, для отображения на странице
		for foto in all_photos:
			pair_photo.append(foto)
			if i%2 == 0 or i == len(all_photos):
				photos.append(pair_photo)
				del pair_photo
				pair_photo = []
			i += 1

 
		if request.user.is_authenticated():

			count_my_photos = UserPhoto.objects.filter(user = request.user).count()

			log_user = request.user
			my_friends, count_my_friends = all_friends(log_user)
			if count_my_friends > 5:
					my_friends = my_friends[:6]

			all_chats = len(list(Chat.objects.filter(author = request.user).order_by('last_change') | Chat.objects.filter(companion = request.user).order_by('last_change')))

			if user==log_user:
				count_new_friends = MyFriends.objects.filter(friend=log_user, status=0).count()
				return render(request, 'person_photo.html', {'person': user, 'log_user': log_user, 'count_new_friends':count_new_friends, 'person_friends':my_friends,'count_friends':count_my_friends, 'count_my_friends':count_my_friends, 'user_photos':photos, 'count_my_photos': count_my_photos, 'count_my_chats': all_chats})
			else:
				is_my_friend = False
				person_friends, count_friends = all_friends(user)
				if user in my_friends:
					is_my_friend = True
				if count_friends > 5:
					person_friends = person_friends[:6]
	

			return render(request, 'person_photo.html', {'person': user, 'log_user': log_user, 'is_my_friend':is_my_friend, 'person_friends':person_friends,'count_friends':count_friends, 'count_my_friends':count_my_friends, 'user_photos':photos, 'count_my_photos': count_my_photos, 'count_my_chats': all_chats})
		else:
			person_friends, count_friends = all_friends(user)
			if count_friends > 5:
					person_friends = person_friends[:6]

			return render(request, 'person_photo.html', {'person': user, 'person_friends':person_friends,'count_friends':count_friends, 'user_photos':photos})
	except MyUser.DoesNotExist:
		return HttpResponse("Данный пользователь не зарегистрирован")


def delete_photo(request):
	''' функция для удаления фото из личного альбома'''
	if request.user.is_authenticated() and request.method == 'POST':
		
		photo_id = request.POST['photo_id']

		try:
			photo = UserPhoto.objects.get(user = request.user, id = photo_id)
			photo.delete()
		except UserPhoto.DoesNotExist:
			pass
		return redirect(request.META["HTTP_REFERER"])
