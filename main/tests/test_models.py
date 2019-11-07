"""tests models.py"""
import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestProject:
    """Tests project model."""
    def test_model(self):
        """test if instance is created."""

        obj = mixer.blend('main.Project')
        assert obj.pk == 1, 'Should create a Project instance'
    def test_str(self):
        """tests __str__ function"""

        obj=mixer.blend('main.Project', name='Master')
        result = str(obj)
        assert result == 'Master', 'Should return name of Project'

    # def test_url(self):
    #     obj=mixer.blend('main.Project')
    #     req = RequestFactory().post('/', {args=[obj.pk,]})
    #     resp =
    #     response = self.client.post(reverse('unit_view', args=[w.pk,])

class TestTemplate:
    """Tests template model."""
    def test_model(self):
        """test if instance is created."""

        obj = mixer.blend('main.Template')
        assert obj.pk == 1, 'Should create a Template instance'
    def test_str(self):
        """tests __str__ function"""

        obj=mixer.blend('main.Template', name='Master')
        result = str(obj)
        assert result == 'Master', 'Should return name of Template'


class TestBlockType:
    """Tests block type model."""
    def test_model(self):
        """test if instance is created."""
        obj = mixer.blend('main.BlockType')
        assert obj.pk == 1, 'Should create a BlockType instance'
    def test_str(self):
        """tests __str__ function"""

        obj=mixer.blend('main.BlockType', name='Master')
        result = str(obj)
        assert result == 'Master', 'Should return name of BlockType'


class TestBlockRequirementBlock:
    """Tests requirement block model"""
    def test_model(self):
        """test if instance is created."""
        obj = mixer.blend('main.RequirementBlock')
        assert obj.pk == 1, 'Should create a Requirement instance'
    def test_str(self):
        """tests __str__ function"""
        blocktype = mixer.blend('main.BlockType', name='Master')
        requirement = mixer.blend('main.Requirement')
        obj=mixer.blend(
            'main.RequirementBlock',
            requirement=requirement,
            blocktype=blocktype
        )
        result = str(obj)
        assert result == '%s Master' % requirement.pk, 'Should return ref and Name of block type'
