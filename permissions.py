from django.contrib.auth.decorators import user_passes_test

def user_can_view(request):
    return request.user.is_authenticated and request.user.has_perm("aa_core_hub.view_structure")

def user_can_manage(request):
    return request.user.is_authenticated and request.user.has_perm("aa_core_hub.change_structure")

require_corehub_view = user_passes_test(lambda u: u.is_authenticated and u.has_perm("aa_core_hub.view_structure"))
require_corehub_manage = user_passes_test(lambda u: u.is_authenticated and u.has_perm("aa_core_hub.change_structure"))
