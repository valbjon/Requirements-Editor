import pytest
from django.contrib.admin.sites import AdminSite
from mixer.backend.django import mixer
from .. import admin
from .. import models
pytestmark = pytest.mark.django_db

#if model admin is used
'''
class TestPostAdmin:
	def test_something:
		site=AdminSite()
		template_admin = admin.TemplateAdmin(models.Template, site)
'''
