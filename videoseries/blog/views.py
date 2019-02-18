from django.shortcuts import render

from django.http import JsonResponse

def blog_list(request):
    context = {
        'title': 'some title here',
        'description': 'some description as well'
    }

    return JsonResponse(context)

def blog_index(request):
    return render(request, "blog/index.html", {})