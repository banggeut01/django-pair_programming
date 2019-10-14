from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from .forms import ArticleForm,CommentForm
from .models import Article, Comment

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-id')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html',context)

def create(request):
    # POST 요청이면,
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        # valid?
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
    # GET 요청이면,
        form = ArticleForm()
        comment_form = CommentForm()
    context = {
        'form' : form,
        'comment_form':comment_form,
    }
    return render(request, 'articles/create.html',context)

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = Comment.objects.filter(article_id=pk)
    context = {
        'article' : article,
        'comments' : comments,
        'comment_form':comment_form,
    }
    return render(request, 'articles/detail.html',context)

def update(request,pk):
    # POST 요청이면,
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        # valid?
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', pk)
    else:
    # GET 요청이면,
        article_form = ArticleForm(instance=article)
    context = {
        'form' : article_form,
        'pk' : pk,
    }
    return render(request, 'articles/update.html',context)

def delete(request,pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')


@require_POST
def comment_create(request,pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.save()
    return redirect('articles:detail', pk)

def comment_delete(request,pk):
    comment = Comment.objects.get(pk=pk)
    article_pk = comment.article_id
    comment.delete()
    return redirect('articles:detail', article_pk)