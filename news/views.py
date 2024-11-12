from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from .forms import SocialMediaLinkForm, CommentForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import NewsPost, Category, Contact, Comment
from django.contrib.auth.decorators import login_required




# Home page view
def home(request):
    """Render the home page."""
    return render(request, 'index.html')


# Contact Us page view
def contact_us(request):
    """Handle the contact form submission and save contact data."""
    if request.method == 'POST':
        contact_data = Contact(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        contact_data.save()
        return redirect('contact_success')
    return render(request, 'contact.html')


# Search News view
def search_news(request):
    """Handle search queries and return results."""
    query = request.GET.get('q')
    results = NewsPost.objects.filter(title__icontains=query) if query else NewsPost.objects.none()
    return render(request, 'search_results.html', {'results': results, 'query': query})


# News list view
def news_list(request):
    """Display a list of all news posts ordered by published date."""
    news_posts = NewsPost.objects.all().order_by('-published_date')
    return render(request, 'news_list.html', {'news_posts': news_posts})


# News detail view
def news_detail(request, pk):
    """Display the details of a specific news post."""
    news_post = get_object_or_404(NewsPost, pk=pk)
    categories = Category.objects.annotate(post_count=Count('news_posts'))
    context = {
        'news_post': news_post,
        'categories': categories,
    }
    return render(request, 'news_detail.html', context)


# Category detail view
def category_detail(request, pk):
    """Display posts under a specific category."""
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'category.html', {'category': category})


# Submit social media link view
def submit_link(request):
    """Handle submission of social media links."""
    if request.method == 'POST':
        form = SocialMediaLinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = SocialMediaLinkForm()
    return render(request, 'submit_link.html', {'form': form})


@login_required
def add_comment(request, pk):
    news_post = get_object_or_404(NewsPost, pk=pk)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news_post = news_post
            comment.user = request.user  # assuming the user is logged in
            comment.save()
            return redirect('news_detail', pk=news_post.pk)
        else:
            # If form is invalid, you can re-render the template with errors
            return render(request, 'news_detail.html', {
                'news_post': news_post,
                'comment_form': comment_form,
            })

    # If not POST request, redirect to the detail page
    return redirect('news_detail', pk=news_post.pk)



# User Signup view
def signup(request):
    """Handle user registration and login upon successful signup."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# Custom login view
def custom_login(request):
    """Handle user authentication and login."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='login')
def news_create(request):
    categories = Category.objects.all()  # Fetch all categories to populate the dropdown

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        author = request.POST.get('author')
        postimage = request.FILES.get('image')  # Handle file uploads with request.FILES

        # Fetch the category object using the ID
        category = Category.objects.get(id=category_id)

        # Create and save the new NewsPost instance
        postData = NewsPost(title=title, content=content, category=category, author=author, image=postimage)
        postData.save()

        return redirect('news_list')
    else:
        return render(request, 'news_form.html', {'categories': categories})
