"""Defines url patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # home page.
    path('', views.index, name='index'),
    # page that shows all topics.
    path('topics/', views.topics, name='topics'),
    # Detail page for a single topic.
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # page for adding a new topic.
    path('new_topic/', views.new_topic, name='new_topic'),
    # page for adding a new entry.
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # page for editiing an entry.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # page for deleting an existing topic.
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    # page for deleting an existing entry.
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    # page for editing a topic.
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    # page showing about informations.
    path('about/', views.about, name='about'),
    # page for showing all entries of a user with respective topics.
    path('contents/', views.contents, name='contents'),
]