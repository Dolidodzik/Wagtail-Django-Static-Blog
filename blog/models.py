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
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.contrib.routable_page.models import RoutablePageMixin, route



# Root/main/home page of whole app under root URL
class BlogIndexPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
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
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('miniature'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        context = super(BlogPage, self).get_context(request)
        context['slider_images'] = self.get_children().specific().first().gallery_images.all()
        context['url'] = self.get_children().specific().first().url
        return context




# Contact

# Social snippet - one social can be twitter/instagram/link to other page
@register_snippet
class Social(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'contact socials'

# Contact page
class ContactPage(Page):

    socials = ParentalManyToManyField('blog.Social', blank=True)

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('socials', widget=forms.CheckboxSelectMultiple),
        ], heading="Socials linked in contact page"),
        StreamFieldPanel('body'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
    ])


# About page is "clone" of homepage, but under diffrent url, and its linked in topbar, unlike blog BlogPage
class About(Page):

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


# Gallery page, preview of this page will be displayed as slider
class GalleryPage(Page):

    # label = "Heading, tags and categories will be auto-inserted"
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(label = "Paragraph")),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        InlinePanel('gallery_images'),
    ]


# Every image in gallery will be instance of this class
class GalleryImage(Orderable):
    page = ParentalKey(GalleryPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    # If true, image will be used in slider in parent page
    ShowInSlider = models.BooleanField(null=True, blank=True)

    panels = [
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('ShowInSlider', widget=forms.CheckboxInput()),
        ])
    ]
