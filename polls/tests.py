import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

"""
You can run tests automatically by running python manage.py test polls
This will find subclasses of django.test.TestCase, create a special
database for testing, and then run the method whose names begin with 
"test"
"""

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class DetailViewTests(TestCase):
    def test_published_question(self):
        """
        If the question is published detail page should be accessible.
        """
        q = create_question('my q', days=-2)
        url = reverse('polls:detail', args=(q.id,))
        response = self.client.get(url)
        self.assertContains(response, q.question_text)

    def test_unpublished_question(self):
        """
        A question that is not yet published should not be accessible.
        """
        q = create_question('my q', days=1)
        url = reverse('polls:detail', args=(q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ResultsViewTests(TestCase):
    def test_published_question(self):
        """
        If the question is published results page should be accessible.
        """
        q = create_question('my q', days=-2)
        url = reverse('polls:results', args=(q.id,))
        response = self.client.get(url)
        self.assertContains(response, q.question_text)

    def test_unpublished_question(self):
        """
        A question that is not yet published should not be accessible.
        """
        q = create_question('my q', days=1)
        url = reverse('polls:results', args=(q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)



class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        _ = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        _ = create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        _ = create_question(question_text="Past question.", days=-30)
        _ = create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        _ = create_question(question_text="Past question 1.", days=-30)
        _ = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )



class QuestionModelTests(TestCase):

    def test_pub_recently_w_future_q(self): 
        """
        Assure that was_pub_recently() returns False for a question 
        published in the future.
        """
        future_date = timezone.now() + datetime.timedelta(days=30)
        future_q = Question(pub_date=future_date)
        self.assertIs(future_q.was_pub_recently(), False)

    def test_pub_recently_w_old_q(self):
        """
        Assure that was_pub_recently returns False for a question 
        published too far in the past.
        """
        past_date = timezone.now() - datetime.timedelta(days=1, seconds=1)
        q = Question(pub_date=past_date)
        self.assertIs(q.was_pub_recently(), False)

    def test_pub_recently_w_recent_q(self):
        """
        Assure that was_pub_recently returns True for a question
        published in the last 24 hours.
        """
        recent_date = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        q = Question(pub_date = recent_date)
        self.assertIs(q.was_pub_recently(), True)