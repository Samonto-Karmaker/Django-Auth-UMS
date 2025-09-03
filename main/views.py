from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegisterForm, PostForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from .models import Post

# Create your views here.
@login_required(login_url='login')
def home(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        if post_id:
            post = get_object_or_404(Post, id=post_id)
            if post.author == request.user or request.user.has_perm('main.delete_post'):
                post.delete()
                print(f"Deleted post with ID: {post_id}")
        return redirect('home')
    return render(request, 'main/home.html', {'posts': posts})

@login_required(login_url='login')
@permission_required('main.add_post', login_url='login', raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'main/create_post.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
