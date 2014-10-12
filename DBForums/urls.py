from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DBForums.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Forum
    url(r'^db/api/forum/create/$', 'api.Views.forum.create', name='create_forum'),
    url(r'^db/api/forum/details/$', 'api.Views.forum.details', name='details_forum'),
    url(r'^db/api/forum/listThreads/$', 'api.Views.forum.list_threads', name='listThreads_forum'),
    url(r'^db/api/forum/listPosts/$', 'api.Views.forum.list_posts', name='listPosts_forum'),
    url(r'^db/api/forum/listUsers/$', 'api.Views.forum.list_users', name='listUsers_forum'),

    # Post
    url(r'^db/api/post/create/$', 'api.Views.post.create', name='create_post'),
    url(r'^db/api/post/details/$', 'api.Views.post.details', name='details_post'),
    url(r'^db/api/post/list/$', 'api.Views.post.post_list', name='list_post'),
    url(r'^db/api/post/remove/$', 'api.Views.post.remove', name='remove_post'),
    url(r'^db/api/post/restore/$', 'api.Views.post.restore', name='restore_post'),
    url(r'^db/api/post/update/$', 'api.Views.post.update', name='update_post'),
    url(r'^db/api/post/vote/$', 'api.Views.post.vote', name='vote_post'),

    # User
    url(r'^db/api/user/create/$', 'api.Views.user.create', name='create_user'),
    url(r'^db/api/user/details/$', 'api.Views.user.details', name='details_user'),
    url(r'^db/api/user/follow/$', 'api.Views.user.follow', name='follow_user'),
    url(r'^db/api/user/unfollow/$', 'api.Views.user.unfollow', name='unfollow_user'),
    url(r'^db/api/user/listFollowers/$', 'api.Views.user.list_followers', name='list_followers'),
    url(r'^db/api/user/listFollowing/$', 'api.Views.user.list_following', name='list_following'),
    url(r'^db/api/user/updateProfile/$', 'api.Views.user.update', name='update_user'),
    url(r'^db/api/user/listPosts/$', 'api.Views.user.list_posts', name='posts_user'),

    # Thread
    url(r'^db/api/thread/create/$', 'api.Views.thread.create', name='create_thread'),
    url(r'^db/api/thread/details/$', 'api.Views.thread.details', name='details_thread'),
    url(r'^db/api/thread/subscribe/$', 'api.Views.thread.subscribe', name='subscribe_thread'),
    url(r'^db/api/thread/unsubscribe/$', 'api.Views.thread.unsubscribe', name='unsubscribe_thread'),
    url(r'^db/api/thread/open/$', 'api.Views.thread.open', name='open_thread'),
    url(r'^db/api/thread/close/$', 'api.Views.thread.close', name='close_thread'),
    url(r'^db/api/thread/vote/$', 'api.Views.thread.vote', name='vote_thread'),
    url(r'^db/api/thread/list/$', 'api.Views.thread.thread_list', name='list_thread'),
    url(r'^db/api/thread/update/$', 'api.Views.thread.update', name='update_thread'),
    url(r'^db/api/thread/remove/$', 'api.Views.thread.remove', name='remove_thread'),
    url(r'^db/api/thread/restore/$', 'api.Views.thread.restore', name='restore_thread'),
    url(r'^db/api/thread/listPosts/$', 'api.Views.thread.list_posts', name='list_posts_thread'),

)
