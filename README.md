# Native admin site with dashboard

### Overview

What do we have here? Another one repainted django admin? Will it works with some
third-party apps which depends on native markup or styles? Will it works after a new
Django released?

I used one of the Django admin app, which has a dashboard, custom styles, javascript
decorations. Lets call this app x-app :) But a week ago was released the new Django v1.9
and 2 days ago I found that my admin became broken.
You will tell me, why don't you fixed a problems and pulled it to x-app repo? Or why
didn't you make an issue. Ok, that's right thinking, but first I should learn about native
Django admin(cause I used it as it is before), then I should learn, how x-app changed
standart functionality of the native admin interface, models uses, whatever.

I've remembered,
how x-app was not compatible with one of translation app, which depends on change form
markup and styles. So I've thought about it, why should I care about this huge repainted admin,
if there is a brand new native(pretty cute designed) and I need only dashboard and maybe
a little more. But using
native functionality, my changes will always works(maybe with a little fixes in a future on a new
Django releases) and all I need is Django documentation and django git repo reading.
That's what it is about :)

### Installing

    # settings.py

    INSTALLED_APPS = (
        # ...

        # 'django.contrib.admin',
        'django.contrib.admin.apps.SimpleAdminConfig', # this one instead above
        'django.contrib.auth',

        # ...
    )

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                # ...

                '/absolute/path/to/native_admin/templates/',

                # ...
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # ...
                ],
            },
        },
    ]

    # for russians:
    LOCALE_PATHS = (
        # ...

        '/absolute/path/to/native_admin/locale/',

        # ...
    )
    # and run in command line: ./manage.py compilemessages

### Admin app

    - apps/
        - admin/
            - model_admin.py
            - admin_site.py

Inherit from:

    # model_admin.py
    from native_admin.admin_model import ModelAdmin


    class BrandAdmin(ModelAdmin):
        list_display = ('title', )

    # ...

Create your admin site:

    # admin_site.py
    from native_admin.admin_site import NativeAdminSite

    from model_admin import BrandAdmin
    from model_admin import ProductAdmin
    from model_admin import ProductFillerAdmin

    from apps.catalog.models import Brand
    from apps.catalog.models import Product
    from apps.catalog.models import ProductFiller


    class MyAdminSite(NativeAdminSite):
        site_header = 'My beatyfull dashboard'

        boards = [
            (u'Products', [
                (Product, ProductAdmin),
                (Brand, BrandAdmin),
                # ...
            ]),
            (u'Products features', [
                (ProductFiller, ProductFillerAdmin),
                # ...
            ]),
        ]

    admin_site = MyAdminSite(name='MyAdminSite')

You will not need in admin.autodiscover() since you used SimpleAdminConfig in settings.py

    # urls.py
    # ...
    from apps.admin.admin_site import admin_site


    urlpatterns = patterns(
        '',
        (r'^admin/', admin_site.urls),
        # ...
    )
