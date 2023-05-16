from django.shortcuts import render, get_object_or_404
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# Cтраница отображения списка заявок(постов)
def post_list(request):
    post_list = Post.published.all()
    # Постраничная разбивка с отображением 5 задач на странице
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если номер страницы не целое число, то выдаем 1 страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница находитсяя вне диапазона, то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)

    return render(request, 'help/post/list.html', {'posts': posts})

# Формирование ссылки поста (ссылка отображает дату создания поста и слаг), отображение полного содержания заявки
def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # Форма для комментариев пользователями
    form = CommentForm()

    return render(request, 'help/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'form': form
                                                     })

# Forms EMAIL

def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} рекомендует прочесть " f"{  post.title }"
            message = f"Прочти {post.title} по {post_url}\n\n" f"{cd['name']} комментарий: {cd['comments']}"
            send_mail(subject, message, 'a09@yandex.ru', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'help/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

# Модель формы комментариев
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'help/post/comment.html', {'post': post,
                                                      'form': form,
                                                      'comment': comment})





