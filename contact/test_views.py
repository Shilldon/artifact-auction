from django.test import TestCase
from django.core import mail
from .views import contact
from .forms import ContactForm

class TestViews(TestCase):

    """test page template used"""
    def test_page_render(self):
        page = self.client.get("/contact/enquiry/")
        self.assertTemplateUsed("contact.html")
    
    """email is sent"""
    def test_email_is_sent(self):
        page = self.client.post("/contact/enquiry/", {"subject": "Enquiry", "enquiry": "Test", "email_address": "test@test.com", "name" : "test"})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,"Enquiry")