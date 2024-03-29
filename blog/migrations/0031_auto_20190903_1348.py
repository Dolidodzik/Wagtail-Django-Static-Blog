# Generated by Django 2.2.3 on 2019-09-03 13:48

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('blog', '0030_galleryimage_gallerypage'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='ShowInSlider',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='GalleryPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='blog.GalleryPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_gallerypagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
