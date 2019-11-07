"""
URLs for main application.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='main-home'),
    #path('editor/<int:pk>/', views.EditorView.as_view(), name='editor'),
    path('editor/<slug:slug>/new', views.RequirementCreateView.as_view(), name='editor-create'),
    path('editor/<slug:slug>/<int:pk>/edit/', views.RequirementUpdateView.as_view(), name='editor-update'),
    path('editor/<slug:slug>/<int:pk>/delete/', views.RequirementDeleteView.as_view(), name='editor-delete'),
    path('projects/', views.ProjectListView.as_view(), name='main-projects'),
    path('templates/', views.TemplateListView.as_view(), name='main-templates'),
    path('template/<int:pk>/', views.TemplateDetailView.as_view(), name='template-detail'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<slug:slug>/select/', views.SelectTemplateView.as_view(), name='select-template'),
    path('project/<slug:slug>/select/<int:pk_t>', views.SubmitTemplateView.as_view(), name='submit-template'),
    path('project/<slug:slug>/delete/', views.ProjectDeleteView.as_view(), name='delete-project'),
    #path('project/<int:pk>/update', views.ProjectUpdateView.as_view(), name='project-update'),
]
