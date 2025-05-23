# Generated by Django 5.1.3 on 2025-05-10 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduklinikapp', '0010_c_notification_linked_to_alter_profile_account_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.BigIntegerField(default=0, verbose_name='amount paid'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='user email'),
        ),
        migrations.CreateModel(
            name='quize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quize_str', models.CharField(blank=True, max_length=500, null=True, verbose_name='quiz id to track do not add this')),
                ('quize_lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduklinikapp.lesson', verbose_name='leasson whit the quiz')),
            ],
        ),
        migrations.CreateModel(
            name='quiz_question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=2000, verbose_name='quiz question')),
                ('option_A', models.CharField(max_length=500, verbose_name='option A')),
                ('option_B', models.CharField(max_length=500, verbose_name='option B')),
                ('option_C', models.CharField(max_length=500, verbose_name='option C')),
                ('link_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduklinikapp.quize', verbose_name='to the quiz the question is lined to')),
            ],
        ),
        migrations.CreateModel(
            name='user_answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_answer', models.CharField(max_length=500, verbose_name='the answer to the question')),
                ('is_corrent', models.BooleanField(default=False, verbose_name='if the answer is correct if not pls leave as node and recore the score in the score board')),
                ('the_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduklinikapp.quiz_question', verbose_name='the question')),
            ],
        ),
    ]
