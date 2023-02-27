import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
from .models import Question

#Models
#Views
class QuestionModelTests(TestCase):
    def setUp(self):
        self.question = Question(question_text="What was the best afition?")
        
    def test_was_publisehed_recently_future_questions(self):
        '''was_published_recently return false for Q whose pub_date is in the future'''
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_publisehed_recently_present_questions(self):
        '''was_published_recently return false for Q whose pub_date is in the present'''
        time = timezone.now()
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)

    def test_was_publisehed_recently_past_questions(self):
        '''was_published_recently return false for Q whose pub_date is in the past'''
        time = timezone.now() - datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

class QuestionIndexViewTests(TestCase):
    def setUp(self):
        self.question = Question(question_text="What was the best afition?")

    def test_no_questions(self):
        '''If no question exists, an appropiate message is displayed'''
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_display_index(self):
        '''If a Q is created with a future pub_date, should not display on index'''
        response = self.client.get(reverse("polls:index"))
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertNotIn(self.question, response.context["latest_question_list"])

    def two_questions_future(self):
        '''If two Q are created with a future pub_date, should not display on index'''
        response = self.client.get(reverse("polls:index"))
        time = timezone.now() + datetime.timedelta(days=30)
        future_Q1 = self.question.pub_date = time
        future_Q2 = self.question.pub_date = time
        self.assertNotIn(future_Q1, future_Q2, response.context["latest_question_list"])

def create_question(question_text, days = 0, hours = 0, minutes = 0, seconds = 0):    
        time = timezone.now() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        future_Q = create_question(question_text="Future Q", days=30)
        url = reverse("polls:detail", args=(future_Q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_Q = create_question(question_text="Past Q", days=-30)
        url = reverse("polls:detail", args=(past_Q.id,))
        response = self.client.get(url)
        self.assertContains(response, past_Q.question_text)

    
        
        




    

