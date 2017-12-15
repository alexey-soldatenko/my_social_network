from django.shortcuts import render, redirect
from django.http import HttpResponse
from auth_user.models import MyUser, MyFriends
from photo.models import UserPhoto
from chat.models import Chat, ChatMessage
import json
from django.template.loader import render_to_string
import datetime


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

def my_chats(user):
	''' функция для определения всех бесед пользователя и соответствующих им сообщениям'''
	all_chats = list(Chat.objects.filter(author = user).order_by('last_change') | Chat.objects.filter(companion = user).order_by('last_change'))
	chats_with_messages = chat_messages(all_chats)
	return chats_with_messages, len(all_chats)

def chat_messages(chats):
	''' функция для сопоставления беседы и относящихся к ней сообщений. Входные данные - список всех бесед, выходные - список кортежей из беседы и соответствующих сообщений.'''
	all_chat_messages = []
	for chat in chats:
		msg = ChatMessage.objects.filter(chat = chat)
		all_chat_messages.append((chat, msg))
	return all_chat_messages




def show_all_my_chats(request):
	''' функция для отображения страницы с беседами и обработки ajax-запросов по извлечению сообщений, а также добавлению новых.'''
	if request.user.is_authenticated():
		if request.method == 'GET':
			#определяем все беседы авторизированного пользователя
			my_friends, count_friends = all_friends(request.user)

			new_friends = MyFriends.objects.filter(friend=request.user, status=0)

			count_new_friends = MyFriends.objects.filter(friend=request.user, status=0).count()

			count_my_photos = UserPhoto.objects.filter(user = request.user).count()

			all_chats, count_my_chats = my_chats(request.user)
			
			return render(request, 'my_chats.html', {'person': request.user, 'my_friends':my_friends, 'new_friends':new_friends, 'count_new_friends':count_new_friends, 'count_my_friends': count_friends, 'person_friends':my_friends,'count_friends':count_friends, 'count_my_photos': count_my_photos, 'all_chats':all_chats, 'count_my_chats':count_my_chats})
		#обрабатываем ajax-запросы в различных режимах
		if request.is_ajax():
			mode = request.POST["mode"]

			if mode == '0':
				#определяем все сообщения запрошенной беседы и передаём её в виде строки html-кода

				chat_id = request.POST["chat_id"]
				chat = Chat.objects.get(id = chat_id)
				messages = ChatMessage.objects.filter(chat = chat)

				ajax_response = render_to_string('chat_messages.html', {'message':messages, 'user': request.user})

				return HttpResponse(ajax_response)

			elif mode == '1':
				#добавляем новое сообщение и извлекаем сообщения из базы со временем размещения больше последнего обновления. Возвращаем новую дату обновления и сообщения в виде строки html-кода.
				text_message = request.POST["message_text"] 
				chat_id = request.POST["chat_id"]

				chat = Chat.objects.get(id = chat_id)

				new_message = ChatMessage(chat = chat, user = request.user, text = text_message)
				new_message.save()

				chat.user_last_change = request.user
				chat.save()

				old_date = datetime.datetime.strptime(request.POST['last_date'], '%d-%m-%Y %H:%M:%S.%f')
				
				new_date = chat.last_change
				new_date = new_date.strftime('%d-%m-%Y %H:%M:%S.%f')
				
				all_new_messages = ChatMessage.objects.filter(chat = chat, date__gt = old_date)
					
				ajax_response = render_to_string('chat_messages.html', {'message':all_new_messages, 'user': request.user})

				data = {'new_date': new_date, 'ajax_response': ajax_response}
				

				return HttpResponse(json.dumps(data), content_type = 'application/json')
			elif mode == '2':
				#автоматический опрос на наличие новых записей, отправляется раз в 5 сек со стороны клиента. Возвращаем новую дату обновления и сообщения в виде строки html-кода.
				try:
					chat_id = request.POST["chat_id"]
					chat = Chat.objects.get(id = chat_id)
					
					old_date = datetime.datetime.strptime(request.POST['last_date'], '%d-%m-%Y %H:%M:%S.%f')

					new_date = chat.last_change
					new_date = new_date.strftime('%d-%m-%Y %H:%M:%S.%f')
					all_new_messages = ChatMessage.objects.filter(chat = chat, date__gt = old_date)
						
					ajax_response = render_to_string('chat_messages.html', {'message':all_new_messages, 'user': request.user})

					data = {'new_date': new_date, 'ajax_response': ajax_response}
				except Exception as err:
					print(err)
				return HttpResponse(ajax_response)
				
	else: 
		return HttpResponse("Вы не авторизированы")
	



def new_message(request):
	''' функция для создания нового сообщения'''
	if request.user.is_authenticated() and request.method == 'POST':
		companion_id = request.POST["companion_id"]
		author_id = int(request.POST["author_id"])
		message_text = request.POST["message_text"]

		author = request.user

		if author_id == request.user.person_id:
			companion = MyUser.objects.get(person_id = companion_id)
		else:
			companion = MyUser.objects.get(person_id = author_id)
		try:
			#проверяем существует ли беседа между текущими пользователями. Так как в модели chat установлено, что author и companion должны быть уникальными, то если в текущем блоке try не возникает исключения, создаем новую беседу.
			chat = Chat(author = author, companion = companion, user_last_change = request.user)
			chat.save()
			print('new_chat')
		except:
			#если беседа существует, находим её, правильно определив кто является автором, а кто собеседником
			chat = Chat.objects.filter(author = author, companion = companion)
			if not len(chat):
				chat = Chat.objects.filter(companion = author, author = companion)[0]
			else:
				chat = chat[0]
		message = ChatMessage(chat = chat, user = author, text = message_text)
		message.save()

		return redirect(request.META["HTTP_REFERER"])
	else:
		return HttpResponse('ВЫ не авторизировались.')


def delete_chat(request):
	''' функция для удаления беседы. Удалить беседу может любой её участник.'''
	if request.user.is_authenticated() and request.method == 'POST':
		chat_id = request.POST["chat_id"]
		try:
			chat = Chat.objects.get(id = chat_id)
			chat.delete()
		except:
			pass
		return redirect(request.META["HTTP_REFERER"])

