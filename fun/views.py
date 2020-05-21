from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone

from fun.forms import LoginForm, SignupForm, PostForm, AuthorForm, CommentForm
from fun.models import Post, Author, Like, Comment


def pagelogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                context = {'form': form,
                           'error': True}
                return render(request, 'registration/login.html', context)
        else:
            context = {'form': form,
                       'error': True}
            return render(request, 'registration/login.html', context)
    else:
        return render(request, 'registration/login.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print('valid')
            user = form.save()
            login(request, user)
            author = Author(user=user, about='', count_posts=0, count_fav=0, fav='', my_fav='')
            author.save()
        else:
            print('not valid')
            flag = True
            form = SignupForm()
            context = {'flag': flag, 'form': form}
            return render(request, 'registration/signup.html', context)
        return redirect('/')
    else:
        form = SignupForm()
        context = {'form': form}
        return render(request, 'registration/signup.html', context)


def get_my_fav(user_id):
    author = Author.objects.get(pk=user_id)
    favorites = author.my_fav
    fav_users = favorites.split(';')
    return fav_users


def get_fav(user_id):
    author = Author.objects.get(pk=user_id)
    favorites = author.fav
    fav_users = favorites.split(';')
    return fav_users


def my_fav(request, user_id):
    fav_list = get_my_fav(user_id)
    favs = []
    error = False
    if fav_list[0] is not '':
        del fav_list[-1]
        for fav in fav_list:
            favs.append(Author.objects.get(pk=fav))
    else:
        error = True
    flag_notification = notification_check(user_id=request.user.id)
    context = {'author': favs, 'error': error, 'flag_notification': flag_notification}
    return render(request, 'fun/my_fav.html', context)


def a_fav(request, user_id):
    fav_list = get_fav(user_id)
    favs = []
    error = False
    if fav_list[0] is not '':
        del fav_list[-1]
        for fav in fav_list:
            favs.append(Author.objects.get(pk=fav))
    else:
        error = True
    flag_notification = notification_check(user_id=request.user.id)
    context = {'author': favs, 'error': error, 'flag_notification': flag_notification}
    return render(request, 'fun/fav_list.html', context)


def author_details(request, username):
    user_id = request.user.id
    flag = False
    flag_fav = False
    auth = True
    if user_id is not None:
        my_favorites = get_my_fav(user_id)
        flag_fav = False
        if user_id == int(username):
            flag = True
        else:
            flag = False
            user_id = int(username)
        for f in my_favorites:
            if f == str(user_id):
                flag_fav = True
                break
            else:
                flag_fav = False
        if request.method == 'POST':
            user = Author.objects.get(pk=user_id)
            author = Author.objects.get(pk=request.user.id)
            if flag_fav:
                user.count_fav = user.count_fav - 1
                user.fav = user.fav.replace(str(author.id) + ';', '')
                user.save()
                author.my_fav = author.my_fav.replace(str(username) + ';', '')
                print(author.my_fav)
                author.save()
                flag_fav = False
            else:
                user.count_fav = user.count_fav + 1
                author_id = str(request.user.id) + ';'
                fav = user.fav
                fav += author_id
                user.fav = fav
                user.save()
                mf = author.my_fav
                print(mf)
                author_id = str(username) + ';'
                mf += author_id
                print(mf)
                author.my_fav = mf
                author.save()
                flag_fav = True
    else:
        auth = False
    s_list = []
    user_id = int(username)
    posts_list = Post.objects.filter(author_id=user_id)
    for p in posts_list:
        s = p.text
        s = s[:444] + '...'
        s_list.append(s)
    author = Author.objects.get(pk=user_id)
    data = zip(posts_list, s_list)
    flag_notification = notification_check(user_id=request.user.id)
    return render(request, 'fun/author_details.html',
                  {'info': author, 'flag': flag, 'auth': auth, 'user_id': user_id, 'data': data,
                   'posts_list': posts_list, 'flag_fav': flag_fav, 'flag_notification': flag_notification})


def edit_author(request, username):
    author = Author.objects.get(pk=request.user.id)
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
        username = form.cleaned_data.get('nickname')
        about = form.cleaned_data.get('about')
        if about is None:
            about = ""
        user.username = username
        user.save()
        author.about = about
        author.save()
        print(about)
        return redirect('/authors/%s/' % author.id)
    else:
        flag_notification = notification_check(user_id=request.user.id)
        return render(request, 'fun/edit_author.html', {'info': author, 'flag_notification': flag_notification})


def posts(request):
    posts_list = Post.objects.all()
    texts_list = []
    for post in posts_list:
        s = post.text
        s = s[:444] + '...'
        texts_list.append(s)
    if posts_list:
        flag = True
    else:
        flag = False
    posts_list = reversed(posts_list)
    texts_list = reversed(texts_list)
    data = zip(list(posts_list), texts_list)
    flag_notification = notification_check(user_id=request.user.id)
    context = {'data': data, 'flag': flag, 'flag_notification': flag_notification}
    return render(request, 'fun/main.html', context)


def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')
            theme = form.cleaned_data.get('theme')
            tags = form.cleaned_data.get('tags')
            pub_date = timezone.now()
            author = Author.objects.get(pk=request.user.id)
            author.count_posts += 1
            author.save()
            count_like = 0
            count_comment = 0
            post = Post(author=author, title=title, text=text, themes=theme, tags=tags,
                        pub_date=pub_date, count_like=count_like, count_comment=count_comment)
            post.save()
            return redirect('/posts/' + str(post.id))
        else:
            flag_notification = notification_check(user_id=request.user.id)
            context = {'form': form, 'flag_notification': flag_notification}
            return render(request, 'fun/new_post.html', context=context)
    else:
        form = PostForm()
        flag_notification = notification_check(user_id=request.user.id)
        context = {'form': form, 'flag_notification': flag_notification}
        return render(request, 'fun/new_post.html', context=context)


def post_details(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post_id=post_id)
    if request.user.id is not None:
        author = Author.objects.get(pk=request.user.id)
        if post.author.id == request.user.id:
            author_flag = True
        else:
            author_flag = False
        likes = Like.objects.filter(author_id=author, post_id=post_id)
        if len(likes) == 0:
            like_flag = False
        else:
            like_flag = True
        if request.method == 'POST':
            if 'like' in request.POST:
                if like_flag:
                    likes.delete()
                    post.count_like -= 1
                    post.save()
                    like_flag = False
                else:
                    post.like_set.create(author=author, flag=True)
                    post.count_like += 1
                    post.save()
                    like_flag = True
            elif 'comment' in request.POST:
                form = CommentForm(request.POST)
                if form.is_valid():
                    text = form.cleaned_data.get('text')
                    pub_date = timezone.now()
                    if request.user.id == post.author.id:
                        comment = Comment(author=author, post=post, text=text, pub_date=pub_date, flag=False)
                    else:
                        comment = Comment(author=author, post=post, text=text, pub_date=pub_date, flag=True)
                    comment.save()
                    return redirect('/posts/' + str(post_id))
        flag_notification = notification_check(user_id=request.user.id)
        context = {'post': post, 'like_flag': like_flag, 'author_flag': author_flag, 'comments': comments,
                   'auth': True, 'flag_notification': flag_notification}
    else:
        flag_notification = notification_check(user_id=request.user.id)
        context = {'post': post, 'like_flag': True, 'author_flag': False, 'comments': comments, 'auth': False,
                   'flag_notification': flag_notification}
    return render(request, 'fun/post_details.html', context)


def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    author = Author.objects.get(pk=post.author.id)
    author.count_posts -= 1
    author.save()
    return redirect('/authors/%s/' % request.user.id)


def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    author = post.author.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
        title = form.cleaned_data.get('title')
        text = form.cleaned_data.get('text')
        post.title = title
        post.text = text
        post.save()
        return redirect('/posts/' + str(post_id))
    else:
        form = PostForm()
        flag_notification = notification_check(user_id=request.user.id)
        return render(request, 'fun/post_edit.html', {'form': form, 'post': post, 'author': author,
                                                      'flag_notification': flag_notification})


def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect('/posts/' + str(post_id))


def notification_check(user_id):
    my_posts = Post.objects.filter(author_id=user_id)
    likes = []
    comments = []
    for p in my_posts:
        likes.append(Like.objects.filter(post_id=p.id, flag=True))
        comments.append(Comment.objects.filter(post_id=p.id, flag=True))
    f_c = ''
    f_l = ''
    if likes:
        f_l = likes[0]
        if len(f_l) != 0:
            f_l = f_l[0]
    if comments:
        f_c = comments[0]
        if len(f_c) != 0:
            f_c = f_c[0]
    if f_c or f_l:
        flag = True
    else:
        flag = False

    return flag


def notification(request):
    user_id = request.user.id
    my_posts = Post.objects.filter(author_id=user_id)
    likes = []
    len_likes = 0
    len_comments = 0
    comments = []
    for p in my_posts:
        likes.append(Like.objects.filter(post_id=p.id, flag=True))
        comments.append(Comment.objects.filter(post_id=p.id, flag=True))
    for like in likes:
        len_likes = len(like)
        for l in like:
            l.flag = False
            l.save()
            print(l.post.title)
    for comment in comments:
        len_comments = len(comment)
        for c in comment:
            c.flag = False
            c.save()
    if comments or likes:
        print('000000')
    context = {'likes': likes, 'comments': comments, 'posts': my_posts}
    return render(request, 'fun/notification.html', context)
