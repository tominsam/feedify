from django.conf import settings # import the settings file

def all_settings(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'settings':settings}
