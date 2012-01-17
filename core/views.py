from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect

import logging

def index(request):
    return render_to_response("index.html", dict(
    ), RequestContext(request))


