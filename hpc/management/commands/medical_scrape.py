import requests
from bs4 import BeautifulSoup
from string import ascii_lowercase
from django.core.management.base import BaseCommand
from django.conf import settings
from collections import OrderedDict

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.med_conditions_scrape()

    def med_conditions_scrape(self):
        medical_conditions = []
        for char in ascii_lowercase:
            r = requests.get('http://www.medicinenet.com/diseases_and_conditions/alpha_' + char + '.htm')
            soup = BeautifulSoup(r.content)
            result_groups = soup.find("div", class_="AZ_results")
            results = result_groups.findAll("li")
            for condition in results:
                medical_conditions.append(condition.string)

        thefile = open('medical_conditions.txt', 'w')
        for condition in medical_conditions:
          thefile.write("%s\n" % condition)
