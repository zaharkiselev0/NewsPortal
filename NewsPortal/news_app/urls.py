from django.urls import path, include
from .views import *
from .decorators import *
from .filters import PostFilter

from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('', get_view(PostList, {paginate: [10]}).as_view(), name='post_list'),
    path('user/<int:pk>/posts/', get_view(PostList, {paginate: [10], by_user: []}).as_view(), name='user_posts'),
    path('news/', get_view(PostList, {paginate: [10], news: []}).as_view()),
    path('articles/', get_view(PostList, {paginate: [10], articles: []}).as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', get_view(PostList, {paginate: [10], filt: [PostFilter]}).as_view()),
    path('news/create/', NewCreate.as_view()),
    path('articles/create/', ArticleCreate.as_view()),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('i18n/', include('django.conf.urls.i18n')), # подключаем встроенные эндопинты для работы с локализацией
] + debug_toolbar_urls()
