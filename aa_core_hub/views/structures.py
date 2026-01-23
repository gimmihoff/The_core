from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from ..models import Structure

@login_required
@permission_required("aa_core_hub.view_structure", raise_exception=True)
def structure_list(request):
    standing = request.GET.get("standing")
    qs = Structure.objects.all()
    if standing:
        qs = qs.filter(standing=standing)
    ctx = {"structures": qs[:500], "standing": standing}
    return render(request, "aa_core_hub/structures.html", ctx)
