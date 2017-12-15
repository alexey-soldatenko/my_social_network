from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from user_records.models import UserRecord, LikeRecord, RepostRecord, CommentRecord, user_directory_path
import json

# Create your views here.
def add_record(request):
	''' функция добавления пользователем новой записи'''
	if request.user.is_authenticated() and request.method == 'POST':
		record_text = request.POST["record_text"]
		if not request.FILES:
			record = UserRecord(user = request.user, author_record = request.user, record_text = record_text)
			record.save()
		else:
			user_image = request.FILES['image']
			record = UserRecord(user = request.user, author_record = request.user, record_text = record_text, image = user_image)
			record.save()
		return redirect(request.META['HTTP_REFERER'])

def delete_record(request):
	''' функция удаления записи пользователем'''
	if request.user.is_authenticated() and request.method == 'POST':
		record_id = request.POST["record_id"]
		try:
			record = UserRecord.objects.get(id = record_id, user = request.user)
			record.delete()
		except UserRecord.DoesNotExist:
			pass
		return redirect(request.META['HTTP_REFERER'])

def add_like(request):
	''' функция обработки ajax-запроса по добавлению лайка 
		к определенной записи. Возвращает новое количество лайков записи.'''
	if request.is_ajax() and request.method == 'POST':
			
		record_id = request.POST['record_id']
		record = UserRecord.objects.get(id = record_id)
		try: 
			like = LikeRecord.objects.get(record_id = record, user = request.user)
		except LikeRecord.DoesNotExist:
			like = LikeRecord(record_id = record, user = request.user, author_record = record.user)
			like.save()
			
		new_count_likes_record = LikeRecord.objects.filter(record_id = record).count()
			
		return HttpResponse(new_count_likes_record)
		

def add_repost(request):
	''' функция обработки ajax-запроса по созданию репоста определенной записи. Создаёт новую запись для текущего пользователя, копирую содержание текущей записи и возвращает новое количество репостов текущей записи.'''
	if request.is_ajax() and request.method == 'POST':
		record_id = request.POST['record_id']
		record = UserRecord.objects.get(id = record_id)
		try: 
			repost = RepostRecord.objects.get(record_id = record, user = request.user)
		except RepostRecord.DoesNotExist:
			repost = RepostRecord(record_id = record, user = request.user, author_record = record.user)
			repost.save()
			new_record = UserRecord(user = request.user, author_record = record.user, record_text = record.record_text, image = record.image)
			new_record.save()
		new_count_repost_record = RepostRecord.objects.filter(record_id = record).count()
		return HttpResponse(new_count_repost_record)

def add_comment(request):
	''' функция обработки ajax-запроса по добавлению 			комментария к определенной записи. Возвращает новое 	количество комментариев записи и html-представление 	самого комментария в виде json-объекта.'''
	if request.is_ajax() and request.method == 'POST':
		
		record_id = request.POST['record_id']
		comment_text = request.POST['comment_text']
		record = UserRecord.objects.get(id = record_id)
		
		comment = CommentRecord(record_id = record, author_record = record.user, user = request.user, text = comment_text)
		comment.save()
		
		response_comment_text = render_to_string('new_comment_message.html', {'comment':comment})
		new_count_comment_record = CommentRecord.objects.filter(record_id = record).count()

		data = {'count_comments':new_count_comment_record, 'html_text':response_comment_text}
		return HttpResponse(json.dumps(data), content_type = 'application/json')
		
