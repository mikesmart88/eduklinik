# Generated by Django 5.1.3 on 2025-05-11 23:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduklinikapp', '0012_remove_transaction_tran_holder'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_tralle',
            field=models.FileField(blank=True, null=True, upload_to='free_file', verbose_name='course trailer shot vedio'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='actton_btn',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='add a text to show in the button do not add the if file is cassifiled as the rest of others this is mainly for the single lesson page'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_dic',
            field=models.TextField(blank=True, null=True, verbose_name='write note and description of the lesson if in single'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_tralle',
            field=models.FileField(blank=True, null=True, upload_to='free_file', verbose_name='lesson trailer shot vedio'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='attribute',
            field=models.CharField(choices=[('lesson note', 'lesson note'), ('past question', 'past question'), ('syllabue', 'syllabue'), ('textbook', 'textbook'), ('handout', 'handout'), ('pdf-ebook', 'pdf-ebook')], max_length=200, null=True, verbose_name='leasson artibute'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='file_package',
            field=models.FileField(blank=True, null=True, upload_to='lesson_files', verbose_name='lesson file package'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='under_course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eduklinikapp.course'),
        ),
    ]
