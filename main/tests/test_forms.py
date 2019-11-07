import pytest
from .. import forms
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

class TestEditorForm:


     def test_init(self):
         #project = mixer.blend('main.Project')
         form = forms.RBForm()
