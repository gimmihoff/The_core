from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import DScan, Structure, StructureTimer
from ..services.structure_logic import get_war_timer_timeline


@login_required
def dashboard(request):
    return render(request, "aa_core_hub/dashboard.html", {
        "structure_count": Structure.objects.count(),
        "timer_count": StructureTimer.objects.count(),
        "dscan_count": DScan.objects.count(),
        "war_timers": get_war_timer_timeline(limit=10),
    })
