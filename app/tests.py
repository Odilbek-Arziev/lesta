from django.test import TestCase, Client
from django.urls import reverse
from .models import UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import unittest
from .utils import process_text


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_file = SimpleUploadedFile(
            "test.txt",
            "Антон жил в маленьком городе. Он любил читать книги.".encode("utf-8"),
            content_type="text/plain",
        )

    def test_index_view_get(self):
        response = self.client.get(reverse("app:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_index_view_post(self):
        response = self.client.post(reverse("app:index"), {"file": self.test_file})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("app:table"))
        self.assertEqual(UploadedFile.objects.count(), 1)

    def test_table_view_without_file(self):
        response = self.client.get(reverse("app:table"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("app:index"))

    def test_table_view_with_file(self):
        uploaded_file = UploadedFile.objects.create(file=self.test_file)
        response = self.client.get(reverse("app:table"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table.html")
        self.assertIn("words", response.context)

    def test_pagination(self):
        UploadedFile.objects.create(file=self.test_file)
        response = self.client.get(reverse("app:table"), {"page": 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn("words", response.context)
        self.assertTrue(hasattr(response.context["words"], "paginator"))


class ProcessTextTest(unittest.TestCase):
    def test_process_text_basic(self):
        text = "Антон жил в маленьком городе. Он любил читать книги. Антон читал много."
        result = process_text(text)

        self.assertGreater(len(result), 0)

        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(result[0]), 3)

        self.assertIsInstance(result[0][1], float)
        self.assertIsInstance(result[0][2], float)

    def test_process_text_stopwords(self):
        text = "И в во не что он на я с со как а то все она так его."
        result = process_text(text)

        self.assertEqual(result, [])

    def test_process_text_ordering(self):
        text = "Город был большим. Город менялся. В городе жили люди."
        result = process_text(text)

        idf_values = [word_data[2] for word_data in result]
        self.assertEqual(idf_values, sorted(idf_values, reverse=True))

    def test_process_text_limit(self):
        text = " ".join([f"слово{i} " * 3 for i in range(100)])
        result = process_text(text)

        self.assertLessEqual(len(result), 50)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    import django

    django.setup()
    TestCase.main()
