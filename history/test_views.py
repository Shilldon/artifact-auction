from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, reverse
from django.utils import timezone
from datetime import timedelta

from .models import Event, Historical_Figure
from artifacts.models import Artifact, Category

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):

        """create 11 artifacts owned by user"""
        category = Category(name="test", description="test")
        category.save()
        number_of_artifacts = 4
        for artifact_id in range(number_of_artifacts):
            artifact = Artifact.objects.create(
                name = f'Name { artifact_id+1 }',
                description = f'Description { artifact_id+1 }',
                type = 'DATA',
                category = category
            )
            """create historical figures for each artifact"""
            for historical_figure_id in range(4):
                Historical_Figure.objects.create(
                    artifact_possessed = artifact,
                    name = f'Historical Figure Artifact { artifact.id } - { historical_figure_id+1 }',
                    description = f'Historical Figure description'
                )
                
            """create events for each artifact"""
            for event_id in range(4):
                Event.objects.create(
                    artifact = artifact,
                    name = f'Historical Event Artifact { artifact.id } - { event_id+1 }',
                    description = f'Event description { event_id+1 } { artifact.name })',
                    historical_figure = get_object_or_404(Historical_Figure, pk=event_id+1)
                )

        """
        create artifact with 1 event
        """
        artifact = Artifact.objects.create(
            name = f'Name { 5 }',
            description = f'Description { 5 }',
            type = 'DATA',
            category = category
        )
        Event.objects.create(
            artifact = artifact,
            name = f'Historical Event Artifact { artifact.id } - { 1 }',
            description = f'Event description { 17 } { artifact.name })',
        )   
    """
    Check display_historical_figure
    """
    
    """
    Check page renders
    """
    def test_display_historical_figure_render(self):
        response = self.client.get('/history/historical_figure/1')
        self.assertEqual(response.status_code, 200)
    
    """
    Check context returned
    """
    def test_historical_figure_context(self):
        response = self.client.get('/history/historical_figure/2')
        self.assertEqual(response.context['historical_figure'].name, "Historical Figure Artifact 1 - 2")        
        self.assertEqual(len(response.context['events']), 4) 
        self.assertEqual(len(response.context['artifacts']), 4)
        
    
    """
    Check display_event
    """
    
    """
    Check page renders
    """
    def test_display_event_render(self):
        response = self.client.get('/history/historical_event/1')
        self.assertEqual(response.status_code, 200)
    
    """
    Check context for artifact with more than 1 event
    """
    
    def test_historical_event_context_more_than_one_event(self):
        response = self.client.get('/history/historical_event/2')
        self.assertEqual(response.context['event'].name, "Historical Event Artifact 1 - 2")        
        self.assertEqual(len(response.context['other_events']), 3) 


    """
    Check context for artifact with only 1 event
    """
    
    def test_historical_event_context_one_event(self):
        response = self.client.get('/history/historical_event/17')
        self.assertEqual(response.context['event'].name, "Historical Event Artifact 5 - 1")        
        self.assertEqual(len(response.context['other_events']), 0) 

  