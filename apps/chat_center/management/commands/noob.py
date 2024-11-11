import random
import uuid
import datetime
from decimal import Decimal
from faker import Faker
from django.utils.text import slugify

from django.core.management import BaseCommand
from django.db.models import Q

from your_app.models import Author, TestField, Book


class Command(BaseCommand):
    def handle(self, *args, **options):
        # author = Author()
        # author.name = 'Hello'
        # author.save()
        #
        # author = Author(name='Hello2')
        # author.save()

        # author = Author.objects.create(name='Hello3')

        # Author.objects.all().__str__()
        # print(Author.objects.filter(name='Hello'))
        # print(Author.objects.filter(name__gt='Hello1'))

        # queryset = Author.objects.filter(name__gt='Hello1')
        # queryset = queryset.filter(name__lt='Hello3')

        # print(queryset)

        # queryset2 = Author.objects.filter(Q(name__gt='Hello1') | Q(name__lt='Hello3'))

        # print(queryset2)

        # queryset3 = Author.objects.exclude(
        #     Q(name__startswith='Hello'),
        #     Q(name__endswith='2') | Q(name__endswith='3')
        # )
        
        # print(queryset3)

        # test = TestField(name='A',gender='M',url='https://www.google.com',email='test@gmail.com',ip='127.0.0.1',message='test')

        # faker = Faker()
        #
        # # Generate data
        # name = faker.name()
        # gender = random.choice(['M', 'F'])
        # url = faker.url()
        # email = faker.email()
        # slug = slugify(name)
        # ipaddress = faker.ipv4()
        # unique_uuid = uuid.uuid4()
        # message = faker.text()
        # date = faker.date()
        # datetime = faker.date_time()
        # duration = timedelta(seconds=random.randint(0, 86400))
        # integer = random.randint(-1000, 1000)
        # positive = random.randint(1, 1000)
        # float_value = random.uniform(0.0, 1000.0)
        # decimal_value = Decimal(random.uniform(0.0, 1000.0)).quantize(Decimal('0.01'))
        #
        # test_field = TestField.objects.create(
        #     name=name,
        #     gender=gender,
        #     url=url,
        #     email=email,
        #     slug=slug,
        #     ipaddress=ipaddress,
        #     uuid=unique_uuid,
        #     message=message,
        #     date=date,
        #     datetime=datetime,
        #     duration=duration,
        #     integer=integer,
        #     positive=positive,
        #     float=float_value,
        #     decimal=decimal_value,
        # )
        #
        # print(f"Created record: {test_field}")

        print(Author.objects.all())


        "query books which author birthdate is today"

        "join"
        books = Book.objects.filter(
            author__birth_date=datetime.date.today(),
        )
        print(books.query)
        for book in books:
            print(book)

        "join (select_related)"
        books = Book.objects.filter(
            author__birth_date=datetime.date.today(),
        ).select_related('author')
        print(books.query)
        for book in books:
            print(book)

        "join (prefetch_related)"
        books = Book.objects.filter(
            author__birth_date=datetime.date.today(),
        ).prefetch_related('author')
        print(books.query)
        for book in books:
            print(book)

        "where in (subquery)"
        # authors = Author.objects.filter(
        #     birth_date=datetime.date.today(),
        # )
        # books = Book.objects.filter(
        #     author__in=authors,
        # )
        # print(books.query)
        # for book in books:
        #     print(book)

        "where in (list)"
        # authors = list(Author.objects.filter(
        #     birth_date=datetime.date.today(),
        # ))
        # books = Book.objects.filter(
        #     author__in=authors,
        # )
        # print(books.query)
        # for book in books:
        #     print(book)

        "where in reverse (subquery)"
        # books = Book.objects.filter(
        #     name__startswith='Harry'
        # )
        # aa = Author.objects.filter(
        #     id__in=books.values('author')
        # )
        # print(aa.query)
        # print(aa.query)


        "join reverse"
        authors = Author.objects.filter(
            books__name__startswith='Hello',
        ).distinct()
        print(authors.query)
        for author in authors:
            print(author)


        "reverse relation manager"
        for author in Author.objects.all():
            print(author.name)
            for book in author.books.all():
                print(' - ',book.name)

        "ถึก"
        book_by_author = {}
        for book in Book.objects.all():
            book_by_author.setdefault(book.author_id, []).append(book)

        for author in Author.objects.all():
            print(author.name)
            for book in book_by_author.get(author.id, []):
                print(' - ', book.name)

        "สบาย"
        for author in Author.objects.all().prefetch_related('books'):
            print(author.name)
            for book in author.books.all():
                print(' - ', book.name)

        "query หนังสือของ author ที่แก่ที่สุด 5 คนแรก"

