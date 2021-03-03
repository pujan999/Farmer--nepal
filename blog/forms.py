from .models import Comments
from django.forms import ModelForm

class CommentCreateForm(ModelForm):
  class Meta:
    model = Comments
    fields = [
      'comments'
    ]


   