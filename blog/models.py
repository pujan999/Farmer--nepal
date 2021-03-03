from django.db import models

# Create your models here.



class Blog(models.Model):
  title = models.CharField(max_length=500,null=True)
  discription = models.TextField(max_length=2000, null=True)
  blog_image = models.ImageField(upload_to='products/')
  post_date =models.DateField(auto_now_add=True,null=True)


  def __str__(self):
    return self.title




class Comments(models.Model):
  blog= models.ForeignKey(Blog,max_length=1500, on_delete=models.CASCADE,null=True)
  comments = models.TextField(max_length=1500, null=True)
  status = models.BooleanField(default=True)
  date_post = models.DateField(auto_now_add=True,null=True)

  def __str__(self):
    return self.blog.title


