import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)

    return Question.objects.create(
        question_text=question_text,
        pub_date=time
    )


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(
            hours=23,
            minutes=59,
            seconds=59
        )

        recent_question = Question(pub_date=time)

        self.assertIs(
            recent_question.was_published_recently(),
            True
        )


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(
            reverse("polls:index")
        )

        self.assertContains(
            response,
            "No polls are available."
        )

    def test_past_question(self):
        question = create_question(
            "Past question",
            -30
        )

        response = self.client.get(
            reverse("polls:index")
        )

        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_future_question(self):
        create_question(
            "Future question",
            30
        )

        response = self.client.get(
            reverse("polls:index")
        )

        self.assertContains(
            response,
            "No polls are available."
        )

    def test_future_question_and_past_question(self):
        question = create_question(
            "Past question",
            -30
        )

        create_question(
            "Future question",
            30
        )

        response = self.client.get(
            reverse("polls:index")
        )

        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )