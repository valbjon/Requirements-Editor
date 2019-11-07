"""Views as in MTV pattern"""
from django.db import transaction
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import Template
from .models import Project
from .models import BlockType
from django.urls import reverse_lazy
from django.forms.models import inlineformset_factory
from .models import (
    Template,
    Project,
    Requirement,
    RequirementBlock,
)
from .forms import  RBForm
import pdb

class ProjectObjectMixin():

    def get_project(self):
        slug = self.kwargs.get('slug')
        obj = None
        if slug is not None:
            obj = get_object_or_404(Project, slug=slug)
        return obj

class FormsetMixin():
    """Provides the functionality to create and populates fields
    inline formsets for Requirements. """
    def get_formset(self, *args):
        if args:
            extra = 0
            instance = self.object
        else:
            extra = len(self.get_project().template.block_types.all())
            instance = None
        if self.request.method == 'POST':
            rb_formset = self.create_rb_formset(extra)
            formset = rb_formset(self.request.POST, instance=self.object)
            return formset
        rb_formset = self.create_rb_formset(extra)
        formset = rb_formset(instance=instance)
        return formset

    def create_rb_formset(self, extra):
        formset =  inlineformset_factory(
            Requirement,
            RequirementBlock,
            form=RBForm,
            fields=['value'],
            can_delete=False,
            extra = extra
        )
        return formset

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        project = context['project']
        block_types = list(project.template.block_types.all())
        with transaction.atomic():
            # set project and save requirement
            form.instance.project = project
            self.object = form.save()
            # set attributes and save requirement blocks
            if formset.is_valid():
                for i, inline_form in enumerate(formset):
                    #transfer blocktype attributes
                    block_type = block_types[i]
                    inline_form.instance.blocktype = block_type
                    inline_form.instance.position = block_type.position
                #associate blocktype with requirment blocks
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)



class HomeView(generic.TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context

class ProjectListView(generic.ListView):

    model = Project
    template_name = 'main/projects.html'
    context_object_name = 'projects'


class ProjectCreateView(generic.CreateView):
    model = Project
    fields = ['name']
    def get_success_url(self):
        return reverse('select-template', kwargs={'slug':self.object.slug})


class SelectTemplateView(ProjectObjectMixin, generic.ListView):

    model = Template
    template_name = 'main/select_template.html'
    context_object_name = 'templates'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.get_project()
        return context

class SubmitTemplateView(ProjectObjectMixin, generic.RedirectView):


    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        project = self.get_project()
        template = get_object_or_404(Template, pk=self.kwargs.get('pk_t'))
        project.template = template
        project.save()
        return reverse('editor-create', kwargs={'slug':project.slug})


class ProjectUpdateView(generic.UpdateView):
    model=Project
    fields = ['name',]
    def get_success_url(self):
        return reverse('main-projects')

class ProjectDeleteView(generic.DeleteView):
    model = Project
    #template_name = 'main/confirm_delete.html'
    def get_success_url(self):
        return reverse('main-projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.object.__class__.__name__
        return context


class TemplateListView(generic.ListView):
    model = Template
    template_name = 'main/templates.html'
    context_object_name = 'templates'


class TemplateDetailView(generic.DetailView):
    model = Template
    context_object_name = 'template'

def editor(request, pk):
    """
    tbd.
    """
    project = Project.objects.get(pk=pk)
    template = project.template
    all_blockTypes = template.block_types.all()

    if template is None:
        return redirect('select-template', pk=pk)

    context = {
        'title': 'Editor',
        'template': template,
        'project': project,
        'all_blockTypes': all_blockTypes
    }
    return render(request, 'main/editor.html', context)
	
class RequirementCreateView(ProjectObjectMixin, FormsetMixin, generic.CreateView):
    template_name = 'main/editor.html'
    model = Requirement
    fields = ()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        project = self.get_project()
        data['project'] = project
        data['title'] = 'Editor'
        data['formset'] = self.get_formset()
        return data

    def get(self, request, *args, **kwargs):
        project = self.get_project()
        if project.template is None:
            return redirect(reverse('select-template', kwargs={'slug': project.slug}))
        return super().get(self, request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse('editor-create', kwargs={
            'slug':self.kwargs.get('slug')
        })


class RequirementUpdateView(ProjectObjectMixin, FormsetMixin, generic.UpdateView):
    template_name = 'main/editor.html'
    model = Requirement
    fields = ()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        project = self.get_project()
        data['project'] = project
        data['title'] = 'Editor'
        data['formset'] = self.get_formset('update')
        return data


    def get_success_url(self, **kwargs):
        return reverse('editor-create', kwargs={
            'slug':self.kwargs.get('slug')
        })

class RequirementDeleteView(ProjectObjectMixin, generic.DeleteView):
    model = Requirement
    def dispatch(self, request, *args, **kwargs):
        self.project = self.get_project()
        return super(RequirementDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy( 'editor-create', kwargs={'slug': self.project.slug})
