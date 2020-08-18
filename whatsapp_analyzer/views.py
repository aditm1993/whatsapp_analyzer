import os

from django.shortcuts import render, redirect
from .utils import analyse_data
from pprint import pprint
import json
import csv
from django.conf import settings


def index(request):
    context = {}
    if request.method == 'POST':
        keywords_text = request.POST['keywords']
        keywords = keywords_text.split(',')
        table_data = analyse_data(keywords)
        pprint(table_data)
        context['table_data'] = table_data
        context['keywords'] = keywords_text
    return render(request, 'index.html', context)


def send_file(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        with open(os.path.join(
                settings.MEDIA_ROOT, 'output_tables', post_data['fileName']
        ), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for row in post_data['data']:
                writer.writerow(row)

    return redirect('index')
