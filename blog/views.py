from datetime import timedelta
from django.shortcuts import render, redirect

# Create your views here.

import random

from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone
from .models import Article, Comment


def index(request):
    if request.method == "POST":
        article = Article(title=request.POST["title"], body=request.POST["text"])
        article.save()
        return redirect(detail, article.id)

    if "sort" in request.GET:
        if request.GET["sort"] == "like":
            articles = Article.objects.order_by("-like")
        else:
            articles = Article.objects.order_by("-posted_at")
    else:
        articles = Article.objects.order_by("-posted_at")

    context = {"articles": articles}

    return render(request, "blog/index.html", context)


def hello(request):
    fortune = random.randint(0, 2)

    isGreatFortune = fortune == 0

    fortuneMessage = ["Great fortune!", "Small fortune", "Bad fortune.."][fortune]

    context = {
        "name": "Alice",
        "weather": "CLOUDY",
        "weather_detail": [
            "Temperature: 30 C",
            "Humidity: 40%",
            "Wind: 5m/s",
        ],
        "isGreatFortune": isGreatFortune,
        "fortune": fortuneMessage,
    }

    return render(request, "blog/hello.html", context)


def redirect_test(request):
    return redirect("hello")


def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    if request.method == "POST":
        comment = Comment(article=article, text=request.POST["text"])
        comment.save()
    context = {"article": article, "comments": article.comments.order_by("-posted_at")}
    return render(request, "blog/detail.html", context)


def update(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Articele does not exist")
    if request.method == "POST":
        article.title = request.POST["title"]
        article.body = request.POST["text"]
        article.save()
        return redirect(detail, article_id)
    context = {"article": article}
    return render(request, "blog/edit.html", context)


def delete(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    article.delete()
    return redirect(index)


def like(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        article.like += 1
        article.save()

    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    return redirect(detail, article_id)


def api_like(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        article.like += 1
        article.save()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    result = {"id": article_id, "like": article}

    return JsonResponse(result)
