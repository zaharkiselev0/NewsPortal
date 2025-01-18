from django.core.management.base import BaseCommand, CommandError
from news_app.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все новости заданных категорий'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('category', nargs='+', type=str)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        self.stdout.readable()
        category_to_delete = options['category']
        self.stdout.write(
            f'Вы действительно хотите удалить все новости категорий {category_to_delete}? y/n')
        answer = input()
        if answer == 'y':
            if category_to_delete[0] == 'all':
                Post.objects.all().delete()
            else:
                categories = Category.objects.all().values_list('category', flat=True)
                for category in category_to_delete:
                    if category not in categories:
                        self.stdout.write(
                            self.style.ERROR(f'Несуществующая категория - {category}'))
                Post.objects.filter(category__category__in=category_to_delete).delete()
            return

