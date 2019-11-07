from django.contrib import admin
from .models import Template
from .models import BlockType
from .models import RequirementBlock
from .models import Project
from .models import Requirement
from .models import TextBlock

class RequirementAdmin(admin.ModelAdmin):
    list_display = ('pk', 'rb_display')

    def rb_display(self, obj):
        return ", ".join([
            rb.value for rb in obj.requirement_blocks.all()
        ])
    rb_display.short_description = 'Blocks'

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'bt_display', 'projects_display')

    def projects_display(self, obj):
        return ", ".join([
            project.name for project in obj.projects.all()
        ])
    projects_display.short_description = 'Projects'

    def bt_display(self, obj):
        return ", ".join([
            bt.name for bt in obj.block_types.all()
        ])
    bt_display.short_description = 'Blocks'

class BlockTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'template_display')

    def template_display(self, obj):
        return ", ".join([
            template.name for template in obj.template_set.all()
        ])
    template_display.short_description = 'Templates'

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'template')


admin.site.register(Requirement, RequirementAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(BlockType, BlockTypeAdmin)
admin.site.register(RequirementBlock)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TextBlock)
