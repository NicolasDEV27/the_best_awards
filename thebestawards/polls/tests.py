import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

#Models
#Views
class QuestionModelTests(TestCase):
    def test_was_publisehed_recently_future_questions(self):
        '''was_published_recently return false for Q whose pub_date is in the future'''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="What was the best afition?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
