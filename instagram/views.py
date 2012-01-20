from instagram.models import AccessToken, InstagramException

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.conf import settings 

import urllib, urllib2
import logging


def index(request):
    if not request.session.get("i"):
        return render(request, "instagram/anon.html", dict(title="instagram"))
    
    try:
        token = AccessToken.objects.get(pk=request.session["i"])
    except AccessToken.DoesNotExist:
        del request.session["i"]
        return HttpResponseRedirect("/instagram/")

    try:
        photos = token.recent_photos()
    except InstagramException, e:
        logging.error("can't talk to instagram: %s"%e)
        return HttpResponseRedirect("/instagram/auth/?logout")

    return render(request, "instagram/list.html", dict(
        title = "instagram",
        token = token,
        photos = photos,
        time = token.last_time,
    ))


def auth(request):
    if request.GET.get("logout") is not None:
        del request.session["i"]
        return HttpResponseRedirect("/instagram/")

    redirect = "%s/instagram/auth/"%settings.SITE_URL

    # bounce step 1
    if not request.GET.get("code") and not request.GET.get("error"):
        return HttpResponseRedirect("%s?client_id=%s&redirect_uri=%s&response_type=code"%(settings.INSTAGRAM_AUTHORIZE_URL, settings.INSTAGRAM_API_KEY, redirect))

    # error in auth. Probably turned us down.
    error = request.REQUEST.get("error")
    if error:
        messages.add_message(request, messages.INFO, "Problem talking to instagram: %s. Try re-doing auth."%error)
        return HttpResponseRedirect("/instagram/")

    # successful auth
    code = request.REQUEST.get("code")
    if code:
        try:
            conn = urllib2.urlopen(settings.INSTAGRAM_ACCESS_TOKEN_URL, urllib.urlencode(dict(
                client_id = settings.INSTAGRAM_API_KEY,
                client_secret = settings.INSTAGRAM_API_SECRET,
                grant_type= "authorization_code",
                redirect_uri= redirect,
                code = code,
            )))
        except urllib2.HTTPError, e:
            messages.add_message(request, messages.INFO, "Problem talking to instagram: %s. Try re-doing auth."%e.read())
            return HttpResponseRedirect("/instagram/")

        # saves the token as well.
        token = AccessToken.from_string(conn.read())

        # keep session small
        request.session['i'] = token.id
        return HttpResponseRedirect("/instagram/")

