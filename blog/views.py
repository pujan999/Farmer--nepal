from django.shortcuts import render,redirect,reverse
from .models import Blog, Comments
from .forms import CommentCreateForm
# Create your views here.
def blogpost(request):
  blog = Blog.objects.all()
 

  context = {"blogs":blog ,}
  return render (request, 'blog.html',context)


def blogdetails(request,pk):
  blog = Blog.objects.get(id=pk or None)
  form = CommentCreateForm()
  comment = Comments.objects.filter(blog_id=pk)

  if request.method == 'POST':
    form = CommentCreateForm(request.POST)

    if form.is_valid():
      obj = form.save(commit=False)
      obj.blog =blog
      obj.save()
      return reverse('blog')


  context = {'blogs':blog ,'comments':comment,'form':form}
  return render(request,'blogdetails.html',context)