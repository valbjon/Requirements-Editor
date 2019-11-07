"""Data structure for ORM."""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Template(models.Model):
    """Provides the strucutre for templates i.e Master.
    """
    name = models.CharField(max_length=100)
    guide = RichTextField()
    image = models.FileField(upload_to='images/', null=True)
    block_types = models.ManyToManyField('BlockType')


    def __str__(self):
        return self.name


class BlockType(models.Model):
    """Provides the strucutre for ´block types i.e liability.
    """
    FIXED = 'FF'
    CHOICE = 'C'
    FREE = 'F'
    KIND_CHOICES = (
        (FIXED, 'Fixed'),
        (CHOICE, 'Choice'),
        (FREE, 'Free')
    )
    name = models.CharField(max_length=100)
    kind = models.CharField(
        max_length=2, choices=KIND_CHOICES,
        default=FIXED,
    )
    position = models.IntegerField()
    text_blocks = models.ManyToManyField('TextBlock')
    deleteAfterSave = models.BooleanField(default=False)
    guide = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['position']



class Project(models.Model):
    """Provides the strucutre for projects.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        related_name='projects',
        blank=True,
        null=True,
        )
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse ('project-update', kwargs={'pk':self.pk})


class RequirementBlock(models.Model):
    """Provides the strucutre for requirement Blocks.
    """
    blocktype = models.ForeignKey(BlockType, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)
    requirement = models.ForeignKey(
        'Requirement',
        on_delete=models.CASCADE,
        related_name='requirement_blocks',
        blank=True,
        null=True,
    )
    position =  position = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return '%s %s' % (self.requirement, self.blocktype)


class Requirement (models.Model):
    """Provides the strucutre for requirements.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='requirements',
    )
    def __str__(self):
        return '%s' %self.pk

class TextBlock(models.Model):

    text = models.CharField(max_length=50)
    guide = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.text
