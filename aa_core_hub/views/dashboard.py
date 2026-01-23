from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import Structure, StructureTimer, DScan

@login_required
def dashboard(request):
    ctx = {
        "structure_count": Structure.objects.count(),
        "timer_count": StructureTimer.objects.count(),
        "dscan_count": DScan.objects.count(),
    }
    return render(request, "aa_core_hub/dashboard.html", ctx)
