"""Chat related views"""


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def room(request, room_name):
    """Returns chat room"""

    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
