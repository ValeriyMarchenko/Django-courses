from django.core.management.base import BaseCommand, CommandError
from sample_app.models import Product, Category
 
 
class Command(BaseCommand):
    help = 'some help for my com'
 
    def add_arguments(self, parser):
        parser.add_argument('category', type=str)
 
    def handle(self, *args, **options):
        answer = input(f'Are you shure you want to delete all posts in this category {options["category"]}? yes/no')
 
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Canceled'))
 
        try:
            category = Category.get(name=options['category'])
            Post.objects.filter(category==category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}')) # в случае неправильного подтверждения говорим, что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {category.name}'))