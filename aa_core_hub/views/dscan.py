from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from ..models import DScan

@login_required
@permission_required("aa_core_hub.view_dscan", raise_exception=True)
def dscan_list(request):
    qs = DScan.objects.all()[:200]
    return render(request, "aa_core_hub/dscan.html", {"dscans": qs})
