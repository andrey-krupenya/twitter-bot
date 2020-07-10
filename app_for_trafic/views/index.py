import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def index_page(request):
    return render(request, "index.html", {})
