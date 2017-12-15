from django.shortcuts import render, redirect
from django.http import HttpResponse
from auth_user.models import MyUser, MyFriends
from user_records.models import UserRecord, LikeRecord, RepostRecord, CommentRecord
from auth_user.forms import ImageForm, SettingForm
from photo.models import UserPhoto
from chat.models import Chat
import os 
from django.conf import settings



def delete_file(path):
	''' Удаление файла из файловой системы '''
	if os.path.isfile(path):
		os.remove(path)


def all_friends(user):
	''' функция для определения общего количества друзей пользователя. Возвращает множество всех друзей и их общее количество.'''
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


def record_info(record):
	''' функция для определения количества лайков, репостов, комментариев. Возвращает количество лайков, репостов, комментариев, а также 5 последних комментариев.'''
	likes = LikeRecord.objects.filter(record_id = record).count()
	reposts = RepostRecord.objects.filter(record_id = record).count()
	comments = CommentRecord.objects.filter(record_id = record).order_by('-date')[:5]
	count_comments = CommentRecord.objects.filter(record_id = record).count()
	return likes, reposts, count_comments, comments


def show_main(request):
	''' функция для отображения главной страницы'''
	return render(request, 'main.html')


def show_person_page(request, person_id):
	''' функция для оотображения страницы пользователя.'''
	try:
		user = MyUser.objects.get(person_id=person_id)
		#определяем все записи пользователя
		all_user_records = UserRecord.objects.filter(user=user).order_by('-date')
		user_records = []
		#для каждой записи находим мета-информацию: количество лайков, репостов, комментариев, сами комментарии
		for record in all_user_records:
			count_likes, count_reposts, count_comments, comments = record_info(record)
			user_records.append((record, count_likes, count_reposts, count_comments, comments))

		if request.user.is_authenticated():
			#если пользователь авторизован, находим его личную информацию: количество друзей, бесед, фото.
			log_user = request.user
			my_friends, count_my_friends = all_friends(log_user)
			if count_my_friends > 5:
					my_friends = my_friends[:6]

			count_my_photos = UserPhoto.objects.filter(user = log_user).count()

			all_chats = len(list(Chat.objects.filter(author = log_user).order_by('last_change') | Chat.objects.filter(companion = log_user).order_by('last_change')))

			if user==log_user:
				count_new_friends = MyFriends.objects.filter(friend=log_user, status=0).count()
				return render(request, 'my_page.html', {'person': user, 'log_user': log_user, 'count_new_friends':count_new_friends, 'person_friends':my_friends,'count_friends':count_my_friends, 'count_my_friends':count_my_friends, 'count_my_photos': count_my_photos, 'user_records':user_records, 'count_my_chats': all_chats})
			else:
				#определяем является ли текущий пользователем другом авторизованного пользователя
				is_my_friend = False
				person_friends, count_friends = all_friends(user)
				if user in my_friends:
					is_my_friend = True
				if count_friends > 5:
					person_friends = person_friends[:6]
				

			return render(request, 'person_page.html', {'person': user, 'log_user': log_user, 'is_my_friend':is_my_friend, 'person_friends':person_friends,'count_friends':count_friends, 'count_my_friends':count_my_friends, 'count_my_photos': count_my_photos, 'user_records':user_records, 'count_my_chats': all_chats})
		else:
			person_friends, count_friends = all_friends(user)
			if count_friends > 5:
					person_friends = person_friends[:6]

			return render(request, 'person_page.html', {'person': user, 'person_friends':person_friends,'count_friends':count_friends, 'user_records':user_records})
	except MyUser.DoesNotExist:
		return HttpResponse("Данный пользователь не зарегистрирован")

def my_settings(request):
	''' функция для отображения страницы настроек пользователя'''
	if request.user.is_authenticated():
		user = request.user
		if request.method == 'POST':
			#проверяем передаёт ли пользователь файл
			if request.FILES:
				if request.FILES['avatar']:
					#проверяем является ли файл картинкой
					form = ImageForm(request.POST, request.FILES)
					if form.is_valid():
						person_image = request.FILES['avatar']
						person_id = form.cleaned_data['person_id']
						#удаляем старое фото, которое являлось аватаром пользователя
						old_path_to_avatar = os.path.join(settings.BASE_DIR, 'media/person/user_%s/avatar/image') %(person_id)
						delete_file(old_path_to_avatar)
						#сохраняем новое фото в качестве аватара
						user.avatar.save('image', person_image)
						user.save()
						return redirect('/my_settings')
						
			else:
				#меняем личные данные пользователя согласно переданным данным
				form = SettingForm(request.POST)	
				if form.is_valid():
					
					person_id = form.cleaned_data['person_id']
					username = form.cleaned_data['username']
					city = form.cleaned_data['city']
					country = form.cleaned_data['country']
					email = form.cleaned_data['email']

					user.city = city
					user.country = country
					user.username = username
					user.email = email
					user.save()
					return redirect('/my_settings')

		return render(request, 'settings.html', {'person':user})
	else:
		return HttpResponse("Вы не авторизированы")

def add_freind(request):
	''' функция для добавления пользователя в качестве друга'''
	if request.method == 'POST' and request.user.is_authenticated():
		friend_email = request.POST['friend']
		try:
			friend = MyUser.objects.get(email=friend_email)
		except MyUser.DoesNotExist:
			pass
		else:
			try:
				friend = MyFriends(man=request.user, friend=friend, status=0)
				friend.save()
			except:
				pass
			return redirect(request.META["HTTP_REFERER"])


def show_person_friends(request):
	''' функция для отображения отображения друзей авторизированного пользователя'''
	if request.user.is_authenticated():
		my_friends, count_friends = all_friends(request.user)

		new_friends = MyFriends.objects.filter(friend=request.user, status=0)

		count_new_friends = MyFriends.objects.filter(friend=request.user, status=0).count()

		count_my_photos = UserPhoto.objects.filter(user = request.user).count()

		all_chats = len(list(Chat.objects.filter(author = request.user).order_by('last_change') | Chat.objects.filter(companion = request.user).order_by('last_change')))
		
		return render(request, 'my_friends.html', {'person': request.user, 'my_friends':my_friends, 'new_friends':new_friends, 'count_new_friends':count_new_friends, 'count_my_friends': count_friends, 'count_my_photos': count_my_photos,
			'count_my_chats': all_chats})
	else: 
		return HttpResponse("Вы не авторизированы")

def accept_refuse_friend(request):
	''' функция для приема или отклонения запроса на дружбу'''
	if request.user.is_authenticated() and request.method == 'POST':
		initiator_email = request.POST['person']
		status = request.POST['status']

		initiator_friendship = MyUser.objects.get(email=initiator_email)

		friendship = MyFriends.objects.get(man=initiator_friendship, friend=request.user)
		if status == 'accept':
			friendship.status = 1
		elif status == 'refuse':
			friendship.status = 2
		friendship.save()

	return redirect('/my_friends')

def page_all_person_friends(request, person_id):
	''' функция для отображения всех друзей текущего пользователя'''
	try:
		user = MyUser.objects.get(person_id=person_id)
	except MyUser.DoesNotExist:
		return HttpResponse('Данный пользователь не зарегистрирован')
	else:
		if request.user.is_authenticated():
			log_user = request.user
			my_friends, count_my_friends = all_friends(log_user)
			count_new_friends = MyFriends.objects.filter(friend=log_user, status=0).count()
			is_my_friend = False
			person_friends, count_friends = all_friends(user)
			if user in my_friends:
				is_my_friend = True

			all_chats = len(list(Chat.objects.filter(author = request.user).order_by('last_change') | Chat.objects.filter(companion = request.user).order_by('last_change')))
			count_my_photos = UserPhoto.objects.filter(user = request.user).count()

			return render(request, 'all_person_friends.html', {'person': user, 'count_new_friends':count_new_friends, 'count_my_friends': count_my_friends, 'person_friends':my_friends, 'is_my_friend':is_my_friend, 'count_my_photos': count_my_photos, 'count_my_chats': all_chats})
		else:
			person_friends, count_friends = all_friends(user)

		

		return render(request, 'all_person_friends.html', {'person': user, 'person_friends':person_friends})

def delete_friendship(request):
	''' функция для удаления дружбы между пользователями'''
	if request.user.is_authenticated() and request.method == 'POST':
		friend_id = request.POST["friend"]
		my_friend = MyUser.objects.get(person_id = friend_id)
		try:
			friend_ship = MyFriends.objects.get(man = request.user, friend = my_friend)
		except MyFriends.DoesNotExist:
			friend_ship = MyFriends.objects.get(man = my_friend, friend = request.user)
		friend_ship.delete()

		return redirect('/my_friends')


def search_page(request):
	''' функция для отображения страницы с результатами поиска.'''
	if request.method == 'GET':

		search_name = request.GET["search_name"]
		all_users = MyUser.objects.filter(username__icontains = search_name)

		if request.user.is_authenticated():
			log_user = request.user
			my_friends, count_my_friends = all_friends(log_user)
			if count_my_friends > 5:
					my_friends = my_friends[:6]

			count_my_photos = UserPhoto.objects.filter(user = log_user).count()

			all_chats = len(list(Chat.objects.filter(author = log_user).order_by('last_change') | Chat.objects.filter(companion = log_user).order_by('last_change')))

			count_new_friends = MyFriends.objects.filter(friend=log_user, status=0).count()
			
			return render(request, 'search.html', {'person': request.user, 'log_user': log_user, 'count_new_friends':count_new_friends, 'person_friends':my_friends,'count_friends':count_my_friends, 'count_my_friends':count_my_friends, 'count_my_photos': count_my_photos, 'count_my_chats': all_chats, 'all_users': all_users})

		else:
		
			return render(request, 'search.html', {'all_users': all_users})
