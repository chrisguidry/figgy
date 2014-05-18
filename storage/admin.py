from django.contrib import admin

from storage.models import Book, Edition, Alias


class InlineAliasAdmin(admin.StackedInline):
    model = Alias
    extra = 0

class InlineEditionAdmin(admin.StackedInline):
    inlines = [InlineAliasAdmin]
    model = Edition
    extra = 0

class BookAdmin(admin.ModelAdmin):
    inlines = [InlineEditionAdmin]

    list_display = ['id', 'list_editions', 'list_aliases']

    def list_editions(self, obj):
        if not obj:
            return

        return ''.join([u'<h3>%s</h3><p>%s</p>' % (e.title, e.description)
                        for e in obj.editions.all()])

    list_editions.allow_tags = True

    def list_aliases(self, obj):
        if not obj:
            return

        rendered_aliases = ''
        for edition in obj.editions.all():
            aliases = sorted(['%s: %s' % (o.scheme, o.value) for o in edition.aliases.all()])
            rendered_aliases += u'<pre>%s</pre>' % '\n'.join(aliases)
        return rendered_aliases

    list_aliases.allow_tags = True

admin.site.register(Book, BookAdmin)


