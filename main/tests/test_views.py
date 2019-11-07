"""tests views.py"""
import pytest
from django.http import Http404
from mixer.backend.django import mixer
from django.test import RequestFactory
from .. import views

pytestmark = pytest.mark.django_db

class TestHomeView():
    def test_anonymous(self):
        req = RequestFactory().get('/')
        resp = views.HomeView.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by anyone'

class TestProjectListView():
    def test_anonymous(self):
        req = RequestFactory().get('/')
        resp = views.ProjectListView.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by anyone'

class TestTemplateListView():
    def test_anonymous(self):
        req = RequestFactory().get('/')
        resp = views.TemplateListView.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by anyone'

class TestRequirementCreateView():
    def test_anonymous(self):
        project = mixer.blend('main.Project')
        template = mixer.blend('main.Template')
        project.template = template
        project.save()
        req = RequestFactory().get('/')
        resp = views.RequirementCreateView.as_view()(req, slug=project.slug)
        assert resp.status_code == 200, 'Should be callable by anyone'

    def test_no_template_selected(self):
        project = mixer.blend('main.Project')
        project.save()
        req = RequestFactory().get('/')
        resp = views.RequirementCreateView.as_view()(req, slug=project.slug)
        assert resp.status_code == 302, 'Should be redirected if no template selected'

    def test_post(self):
        template = mixer.blend('main.Template')
        project = mixer.blend('main.Project', template=template)
        template.block_types = mixer.cycle[3].blend('main.BlockType')
        requirement = mixer.blend('main.Requirement')
        requirement.requirement_blocks = mixer.cycle[3].blend('main.BlockType')

class TestTemplateDetailView():
    def test_with_object(self):
        obj = mixer.blend('main.Template')
        req = RequestFactory().get('/')
        resp = views.TemplateDetailView.as_view()(req, pk=obj.pk)
        assert resp.status_code == 200, 'Should be callable by anyone'

    def test_no_object(self):
        req = RequestFactory().get('/')
        with pytest.raises(Http404):
            views.TemplateDetailView.as_view()(req, pk=1)


class TestProjectCreateView():
    def test_post(self):
        data = {'name': 'New Project Text'}
        req = RequestFactory().post('/', data=data)
        resp = views.ProjectCreateView.as_view()(req)
        assert resp.status_code ==302, 'Should redirect to success view'
        #assert resp == '/project/%i/select/' %
        # self.assertRedirects(response, 'blog/new-blog/‘)


class TestSelectTemplateView():
    def test_with_object(self):
        req = RequestFactory().get('/')
        obj = mixer.blend('main.Project')
        resp = views.SelectTemplateView.as_view()(req, pk=obj.pk)
        assert resp.status_code == 200, 'Should be callable by anyone'

    def test_no_object(self):
        req = RequestFactory().get('/')

        with pytest.raises(Http404):
            views.SelectTemplateView.as_view()(req, slug='test-slug')

class TestSubmitTemplateView():
    def test_anonymous(self):
        req = req = RequestFactory().get('/')
        project = mixer.blend('main.Project')
        template = mixer.blend('main.Template')
        resp = views.SubmitTemplateView.as_view()(req, slug=project.slug, pk_t=1)
        assert resp.status_code == 302, 'Should redirect to success view'

    def test_no_project(self):
        req = RequestFactory().get('/')
        template = mixer.blend('main.Template')
        with pytest.raises(Http404):
            views.SubmitTemplateView.as_view()(req, slug='test-slug', pk_t=template.pk)

    def test_no_template(self):
        req = RequestFactory().get('/')
        project = mixer.blend('main.Project')
        with pytest.raises(Http404):
            views.SubmitTemplateView.as_view()(req, pk=project.pk, pk_t=1)

    def test_no_objects(self):
        req = RequestFactory().get('/')
        with pytest.raises(Http404):
            views.SubmitTemplateView.as_view()(req, pk=1, pk_t=1)

    class TestRequirementUpdateView():

        def test_anonymous(self):
            project = mixer.blend('main.Project')
            requirement = mixer.blend('main.Requirement')
            req = RequestFactory().get('/')
            resp = views.RequirementUpdateView.as_view()(req, slug=project.slug, pk=requirement.pk)
            assert resp.status_code == 200, 'Should be callable by anyone'

        def test_no_project(self):
            requirement = mixer.blend('main.Requirement')
            req = RequestFactory().get('/')
            with pytest.raises(Http404):
                views.RequirementUpdateView.as_view()(req, slug='project-slug', pk=requirement.pk)

        def test_no_requirement(self):
            project = mixer.blend('main.Project')
            req = RequestFactory().get('/')
            with pytest.raises(Http404):
                views.RequirementUpdateView.as_view()(req, slug=project.slug, pk=1)

        def test_no_objects(self):
            req = RequestFactory().get('/')
            with pytest.raises(Http404):
                views.RequirementUpdateView.as_view()(req, slug='project_slug', pk=1)
