from random import randint
from jokes import JOKES


def clean_ret():
    def wrapper(*args, **kwargs):
        request = args[0] or kwargs['request']
        context = request['context']
        context['ret'] = ''
    return wrapper


def necessary_entities(entities):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            request = args[0] or kwargs['request']
            request_entities = request['entities']
            for entity in entities:
                if entity not in request_entities.keys():
                    request['context']['ret'] = "I need to know " + entity
                    return request['context']
            return function(*args, **kwargs)
        return wrapper
    return real_decorator


def random_joke(function):
    def wrapper(*args, **kwargs):
        request = args[0] or kwargs['request']
        context = function(*args, **kwargs)
        if 'humour_percent' not in context.keys():
            context['humour_percent'] = 0
        if randint(0,1000) / 1000 < context['humour_percent']:
            context['joke'] = ' \n ' + JOKES[randint(0,1000) % len(JOKES)]
        else:
            context['joke'] = ""
        return context
    return wrapper
