from django.views.decorators.cache import cache_page
from django.core.cache import cache


def news(view):
    view.queryset = view.queryset.filter(article=False)


def articles(view):
    view.queryset = view.queryset.filter(article=True)


def by_user(view):
    old_get_queryset = view.get_queryset

    def get_queryset(self):
        queryset = old_get_queryset(self)
        queryset = queryset.filter(puser__pk=self.kwargs['pk'])
        return queryset

    view.get_queryset = get_queryset


def paginate(view, n: int):
    view.paginate_by = n
    view.extra_context['after'].append('elements/paginate.html')


def filt(view, filter_class):
    old_get_queryset = view.get_queryset

    def get_queryset(self):
        queryset = old_get_queryset(self)
        filterset = filter_class(self.request.GET, queryset)
        self.extra_context['filterset'] = filterset
        return filterset.qs

    view.get_queryset = get_queryset
    view.extra_context['before'].append('elements/filter.html')


# def cash_time(view, seconds: int):
#     old_as_view = view.as_view
#
#     def as_view():
#         return cache_page(seconds)(old_as_view())
#     view.as_view = as_view
#
#
# def cash_save(view):
#     old_get_obj = view.get_object
#
#     def get_object(self, *args, **kwargs):
#         obj = cache.get(f'{view.model}-{self.kwargs["pk"]}', None)
#         if not obj:
#             obj = old_get_obj(self, queryset=self.queryset)
#             cache.set(f'{view.model}-{self.kwargs["pk"]}', obj)
#         return obj
#
#     view.get_object = get_object
