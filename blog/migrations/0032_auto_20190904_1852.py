# Generated by Django 2.2.3 on 2019-09-04 18:52

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_auto_20190903_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallerypage',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='gallerypage',
            name='tags',
        ),
        migrations.AlterField(
            model_name='gallerypage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock(label='Paragraph'))]),
        ),
        migrations.DeleteModel(
            name='GalleryPageTag',
        ),
    ]
