from django.contrib import admin

from storage.models import Book, Alias


class InlineAliasAdmin(admin.StackedInline):
    model = Alias
    extra = 0


class BookAdmin(admin.ModelAdmin):
    inlines = [InlineAliasAdmin]

    list_display = ['id', 'title', 'list_aliases']

    def list_aliases(self, obj):
        if obj:
            aliases = sorted(['%s: %s' % (o.scheme, o.value) for o in obj.aliases.all()])
            return u'<pre>%s</pre>' % '\n'.join(aliases)

    list_aliases.allow_tags = True

admin.site.register(Book, BookAdmin)


