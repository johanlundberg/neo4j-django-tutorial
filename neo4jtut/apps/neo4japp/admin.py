from django.contrib import admin
from apps.neo4japp.models import Movie, Person

# Register your models here.

class NodeHandleAdmin(admin.ModelAdmin):
    actions = ['delete_object']

    # Remove the bulk delete option from the admin interface as it does not
    # run the NodeHandle delete-function.
    def get_actions(self, request):
        actions = super(NodeHandleAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_object(self, request, queryset):
        """
                As we extended the NodeHandle delete method we need to have our bulk delete method in the admin
                interface call delete for each object.
                """
        deleted = 0
        for obj in queryset:
            obj.delete()
            deleted += 1
        if deleted == 1:
            message_bit = "1 NodeHandle was"
        else:
            message_bit = "%s NodeHandles were" % deleted
        self.message_user(request, "%s successfully deleted." % message_bit)

    delete_object.short_description = "Delete the selected NodeHandle(s)"


class MovieAdmin(NodeHandleAdmin):
    pass


class PersonAdmin(NodeHandleAdmin):
    pass

admin.site.register(Movie, MovieAdmin)
admin.site.register(Person, PersonAdmin)
