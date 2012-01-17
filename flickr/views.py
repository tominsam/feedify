from flickr.models import RequestToken, AccessToken, EXTRAS
from flickr.feeds import PhotoFeed

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.conf import settings 

import oauth2
import urllib
import logging


# decorator, for some reason
def flickr_auth(fn):
    def wrapper(request, *args, **kwargs):
        request.access_token = None
        if request.session.get("fa"):
            try:
                request.token = AccessToken.objects.get(id=request.session['fa'])
            except AccessToken.DoesNotExist:
                logging.info("bad access token %s"%request.session['fa'])
                del request.session['fa']
        return fn(request, *args, **kwargs)
    return wrapper


@flickr_auth
def index(request):
    if not hasattr(request, "token"):
        return render(request, "flickr_anon.html")

    no_instagram = request.REQUEST.get("no_instagram")
    just_friends = request.REQUEST.get("just_friends")
    include_self = request.REQUEST.get("include_self")

    photos = request.token.recent_photos(
        no_instagram=no_instagram,
        just_friends=just_friends,
        include_self=include_self,
    )

    return render(request, "flickr.html", dict(
        title = "flickr",
        token = request.token,
        photos = photos,
        time = request.token.last_time,
    ))




def auth(request):
    consumer = oauth2.Consumer(key=settings.FLICKR_API_KEY, secret=settings.FLICKR_API_SECRET)

    if request.GET.get("logout") is not None:
        del request.session["fa"]
        return HttpResponseRedirect("/flickr/")

    # bounce step 1
    if not request.GET.get("oauth_token"):
        client = oauth2.Client(consumer)
        # callback url support! SO AWESOME.
        params = urllib.urlencode(dict(oauth_callback = settings.SITE_URL+"/flickr/auth/",))
        resp, content = client.request("%s?%s"%(settings.FLICKR_REQUEST_TOKEN_URL, params), "GET")

        if resp['status'] != '200':
            messages.add_message(request, messages.INFO, "Error talking to flickr: (%s) %s"%(resp['status'], content[:100]))
            return HttpResponseRedirect("/flickr/")
        
        request_token = RequestToken.from_string(content)

        # keep session small
        request.session['fr'] = request_token.id
        return HttpResponseRedirect("%s?perms=read&oauth_token=%s"%(settings.FLICKR_AUTHORIZE_URL, request_token.key))


    else:
        # step 2
        try:
            rt = RequestToken.objects.get(key = request.GET.get("oauth_token"))
        except RequestToken.DoesNotExist:
            messages.add_message(request, messages.INFO, "Bad token when talking to flickr. Try re-doing auth.")
            return HttpResponseRedirect("/flickr/")

        if rt.id != request.session.get('fr', None):
            logging.warn("tokens %r and %r do not match"%(rt.id, request.session.get('fr', "(None)")))
            messages.add_message(request, messages.INFO, "Bad token when talking to flickr. Try re-doing auth.")
            return HttpResponseRedirect("/flickr/")

        token = rt.token()
        token.set_verifier(request.GET.get("oauth_verifier"))
        client = oauth2.Client(consumer, token)

        resp, content = client.request(settings.FLICKR_ACCESS_TOKEN_URL, "POST")
        if resp['status'] != '200':
            messages.add_message(request, messages.INFO, "Error talking to flickr: (%s) %s"%(resp['status'], content[:100]))
            return HttpResponseRedirect("/flickr/")

        # this creates/updates a token object about this user. It's the user record, for all intents and purposes.
        access_token = AccessToken.from_string(content)

        # keep session small
        request.session['fa'] = access_token.id
        if 'fr' in request.session:
            del request.session['fr']
        return HttpResponseRedirect("/flickr/")





