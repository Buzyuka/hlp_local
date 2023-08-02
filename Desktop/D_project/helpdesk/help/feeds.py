import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostFeed(Feed):
    title = 'Мои задачи'
    link = reverse_lazy('help:post_list')
    description = 'Мои новые задачи'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body),30)

    def item_pubdate(self, item):
        return item.publish