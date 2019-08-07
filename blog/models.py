from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.snippets.models import register_snippet
from django import forms
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from django.shortcuts import render



# Root/main/home page of whole app under root URL
class BlogIndexPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),

        ('gallery', blocks.StreamBlock(
            [
                ('image', ImageChooserBlock()),
            ], label='image gallery' )),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


# Tag that SHOULD be used in each BlogPage
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

# Category of BlogPage (similiar to tag)
@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'



# Standard blog page with text/images etc.
class BlogPage(Page):
    date = models.DateField(auto_now=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    miniature = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='miniature'
    )

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),

        ('gallery', blocks.StreamBlock(
            [
                ('image', ImageChooserBlock()),
            ], label='image gallery' )),
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('miniature'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        StreamFieldPanel('body'),
    ]
