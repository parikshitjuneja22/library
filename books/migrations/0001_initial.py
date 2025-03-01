# Generated by Django 5.1.3 on 2024-11-10 10:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=50)),
                ('published_date', models.DateField()),
                ('isbn', models.CharField(max_length=13, unique=True)),
                ('available', models.BooleanField(default=True)),
                ('borrow_count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('membership_date', models.DateField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Borrower',
                'verbose_name_plural': 'Borrowers',
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_date', models.DateField(default=django.utils.timezone.now)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('is_returned', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.borrower')),
            ],
            options={
                'verbose_name': 'Loan',
                'verbose_name_plural': 'Loans',
            },
        ),
    ]
