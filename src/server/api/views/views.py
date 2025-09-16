import json
import logging
from time import sleep

import keyboard
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("hijacker.app")


@csrf_exempt
def send_target(request):
    if request.method == 'GET':
        return JsonResponse({'status': 'ok', 'target': input("Enter the target: ")})


@csrf_exempt
def recv_hijacked_msg(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if "message" not in data:
                return JsonResponse({'status': 'error', "message": "Missing message"}, status=400)
            logger.info(f"Hijacked message: {data['message']}")
            keyboard.write(data['message'])
            keyboard.press_and_release("enter")
            return JsonResponse({'status': 'ok'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', "message": "Invalid JSON"}, status=400)

    return JsonResponse({'status': 'error', "message": "Invalid request method"}, status=405)
