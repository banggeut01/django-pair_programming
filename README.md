# 웹 - django test 대비

* 초기 설정

  ```shell
  python -m venv venv
  activate
  pip install django
  django-admin startproject rereboot .
  python manage.py runserver
  python manage.py startapp articles # 앱이름 복수형
  settings.py 에 앱 등록
  ```

  여기서 팁은 터미널 두개로 1. runserver 화면과 2. shell 화면 띄워둔다.

* 모델 정의

  ```python
  # from django.db import models
  
  class Article(models.Model): # 모델은 단수형, models 앱안에 있는 Model
      title = models.CharField(max_length=20)
      content = models.TextField()
      created_at = models.DateTimeFeild(auto_now_add=True) # 지금 시간 & 추가될 때
      updated_at = models.DateTimeFeild(auto_now=True) # 지금 시간
  ```

  ```shell
  python manage.py makemigrations
  python manage.py migrate
  # 모델 만들어졌는지 확인하기
  python manage.py showmigrations
  [x] # => 모델 정의 제대로 된 것
  ```

* url 정의 (지금 폴더 내에 urls.py)

  ```python
  from django.urls import include
  
  urlpatterns = [
      path('articles/', include('articles.urls'))
  ]
  ```

* articles > urls.py 만들기

  ```python
  from django.urls import path
  from . import views
  
  app_name = 'articles' #처음부터 url app name 설정
  
  urlpatterns = [
      path('', views.index, name='index'),
  ]
  ```

  여기까지 하면 오류가 뜬다. => 정상

* views.py

  ```python
  from .models import Articles
  
  def index(request):
      articles = Aritcle.objects.all()
      context = {
          'articles': articles
      }
      # render(request, 템플릿의 위치, (넘길값))
      return render(request, 'articles/index.html', context) 
  ```

* 템플릿 만들기 articles > templates > articles > index.html

  ```
  # 웹 오류 메시지
  TemplateDoesNotExist at /articles/
  articles/index.html
  ```

  url을 보고 urls.py에서 index함수인 것을 확인

  views.py 에서 index함수의 return 값을 본다.

  템플릿 위치 매칭

* base.html block 지정

  ```html
  <!DOCTYPE html>
  <html lang="ko">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="{% static 'articles/style.css' %}">
  </head>
  <body>
    {% block 블럭이름 %}
    {% endblock %}
  </body>
  </html>
  ```

  * base.html 쓸 때

    ```html
    {% extends 'articles/base.html' %} <!-- 경로 주의 -->
    
    {% block 블럭이름 %}
      <h1>
          Hello,
      </h1>
    {% endblock %}
    ```

* urls.py

  ```python
  path('create/', views.create, name='create'),
  ```

* views.py

  ```python
  def create(request):
      pass
  ```

* 모델 폼 만들기 articles > forms.py

  ```python
  from django import forms
  from .models import Article
  
  class ArticleForm(forms.ModelForm): # 가져올모델Form
      class Meta:
          model = Article # Article 모델 import 했는지
          fields = ('title', 'content')
  ```

* views.py

  ```python
  from . import ArticleForm
  def create(request):
      # form 만들기
      form = ArticleForm()
  	context = {
          'form': form
      }
      return render(request, 'articles/create.html', context)
  ```

* form 출력해보기 create.html 작성

  ```html
  {% extends 'articles/base.html' %} <!-- 경로 주의 -->
  
  {% block 블럭이름 %}
  <form action="" method="POST"> <!-- 2. 묶여있지 않은 것을 보고 묶어주기 -->
      {{ form }} <!-- 1. form 출력해보기 -->
      {% csrf_token %}
      <input type="submit" value="제출">
  </form>
    
  {% endblock %}
  ```

  웹 오류 404, csrf 토큰 오류 확인하고 수정하기 `{% csrf_token %}`추가

* create 함수 수정

  ```python
  def create(request):
      if request.method == 'POST':
          article_form = ArticleForm(request.POST) # POST로 받아온 요청 인자
          if article_form.is_valid(): # 괄호 주의! 함수
              article = article_form.save() # save() return 값 => class의 instance
              return redirect('articles:index') # render가 아닌 redirect 주의!
      else:
      	article_form = ArticleForm() # 수정하기는 인자에 instance=article주의
  	context = {
          'article_form': article_form
      }
      return render(request, 'articles/create.html', context) # render는 
  ```

  * redirect vs render
    * 가장 큰 차이점은 render는 그렇게 보이는 '척'을 하는 것이다.
    * redirect를 통해 해당 경로로 보내는 것이 좋다.

* update 작성, #: create와 비교해 다른 곳

  ```python
  from django.shortcuts import get_object_or_404
  def update(request, article_pk): #
      article = get_object_or_404(Article, pk=article_pk) #import
      if request.method == 'POST':
          article_form = ArticleForm(request.POST, instance=article) # 
          if article_form.is_valid(): 
              article = article_form.save() 
              return redirect('articles:index') 
      else:
      	article_form = ArticleForm(instance=article) # 
  	context = {
          'article_form': article_form
      }
      return render(request, 'articles/create.html', context) # create.html 같이 사용해도 된다.
  ```

* **comment**

  ```python
  comment = Comment()
  comment.content = request.POST.get('content') # 사용자가 form
  comment.article = article # 내가 직접
  comment.save() # 저장 끝!
  
  comment_form = CommentForm(request.POST) # 사용자가 form + modelform
  comment_form.save()
  # 오류! Not null constraint -> FK 넣어!
  
  comment_form = CommentForm(request.POST) # 사용자가 form + modelform
  comment = comment_form.save(commet=False) # 저장 잠깐만!(DB에 쿼리 날리지 말고) comment 인스턴스 줘!
  comment.article = article # 내가 직접
  comment_form.save() # DB에 쿼리
  ```
