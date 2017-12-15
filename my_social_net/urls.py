from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'my_social_net.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'views.show_main'),

    #персонализация
    url(r'^signup_save$', 'auth_user.views.signup_save'),
    url(r'^signup$', 'auth_user.views.signup_page'),
    url(r'^login$', 'auth_user.views.user_login'),
    url(r'^logout$', 'auth_user.views.user_logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'auth_user.views.activate_account', name='activate'),

    #страница пользователя
    url(r'^person/id_(?P<person_id>[\d]+)$', 'views.show_person_page'),
    url(r'^person/id_(?P<person_id>[\d]+)/friends$', 'views.page_all_person_friends'),
   
    #для авторизированного пользователя
    url(r'^my_settings$', 'views.my_settings'),
    url(r'^add_freind$', 'views.add_freind'),
    url(r'^delete_friend', 'views.delete_friendship'),
    url(r'^my_friends$', 'views.show_person_friends'),
    url(r'^accept_refuse_friend$', 'views.accept_refuse_friend'),
    url(r'^add_record$', 'user_records.views.add_record'),
    url(r'^delete_record$', 'user_records.views.delete_record'),
    url(r'^add_like$', 'user_records.views.add_like'),
    url(r'^add_repost', 'user_records.views.add_repost'),
    url(r'^add_comment', 'user_records.views.add_comment'),
    url(r'person/id_(?P<person_id>[\d]+)/photo$', 'photo.views.person_photo'),
    url(r'^delete_photo$', 'photo.views.delete_photo'),
    url(r'^my_chats$', 'chat.views.show_all_my_chats'),
    url(r'^new_message$', 'chat.views.new_message'),
    url(r'^delete_chat$', 'chat.views.delete_chat'),

    #поиск
    url(r'^search', 'views.search_page'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

