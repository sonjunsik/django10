from django.shortcuts import render
from django.views.generic.list import ListView

# Create your views here.

# 제네릭뷰 : 장고에서제공하는 여러가지 뷰기능을 수행하는 클래스  (클래스 기반 뷰정의, 기존까지는 함수기반 뷰정의)
# class뷰이름(제네릭뷰 상소):
# 상속받은 제네릭뷰 클래스의 변수/메소드를 수정해 사용
# 단, 해당 제네릭뷰가 어떤 기능을 수행하는지, 어떤 변수/ 삼수를 사용할수 있는지 파악해야함.
# ListView : 특정모델클래스의 객체의 목록을 다루는 기능을 수행하는 뷰클래스
# DetailView : 특정 모델클래스의 객체 하나를 템플릿에 전달할 때 사용하는 뷰클래스
from .models import Post, PostFile, PostImage
from django.views.generic.detail import DetailView
# 게시물 목록(index)
class Index(ListView):
    template_name ='blog/index.html'   #HTML 파일의 경로를 저장하는 변수
    model = Post            #목록으로 보여질 모델클래스를 저장하는 변수
    context_object_name='post_list'  #템플릿에 객체를 넘겨줄때 사용할 변수이름(사전형 키값)
    paginate_by = 5     #한페이지에 몇개의 객체를 보여줄지 설정

#상세 페이지(detail)
class Detail(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    context_object_name ='obj'
    
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse


from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin #비로그인 상태의 유저를 로그인페이지로 이동
from django.views.generic.edit import FormView #폼클래스를 사용하는 객체로 생성해 템플릿으로 넘겨주는 뷰
#글 등록 페이지(PostRegist)
class PostRegiste(LoginRequiredMixin, FormView):
    template_name ='blog/postregiste.html'
    form_class = PostForm
    context_object_name ='form'
    #FormView는 내부적으로  GET 방식으로 요청한 클라이언트에게 지정된 폼 클래스의 객체를 넘겨줌
    #POST방식으로 요청한 클라이언트를 구분하며, is_valid 까지 수행을 함
    
    #is_valid()함수가  True를 반한했을 때에 대한 처리를 오버라이딩으로 구현
    
    def form_valid(self, form):
        obj = form.save(commit=False) #obj: Post 객체(데이터베이스에 저장X)
        obj.author = self.request.user #유저정보 채우기
        obj.save()    # 데이터베이스에 Post객체 저장
        
        #사용자가 저장요청한 이미지파일, 파일을 객체로 만들어 저장
        #<form>태그 중 name이 'images'인 파일데이터를 추출하는 방식
        for f in self.request.FILES.getlist('images'):
            #PostImage 객체를 생성
            #객체 생성시 각 변수에 값을 채워넣는 작업을 수행함.
            image = PostImage(post=obj, image=f)
            #image = PostImage()
            #image.post = obj
            #image.image = f
            image.save()
        for f in self.request.FILES.getlist('file'):
            file = PostFile(post=obj, file=f)
            file.save()   
                        
        return HttpResponseRedirect(reverse('blog:detail', args=(obj.id,)))
    
    
    