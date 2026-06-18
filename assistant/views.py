from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import requests
import json

@login_required
def assistant_view(request):
    return render(request, 'assistant/assistant.html')

@login_required
def ask_question(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question', '')

        if not question:
            return JsonResponse({'error': 'No question provided'}, status=400)

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": "openrouter/auto",
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a compassionate health assistant for cancer patients on the Oncocare platform.
You provide clear, simple, easy to understand explanations.
Always remind patients to consult their doctor for medical decisions.
Never diagnose or prescribe medication.
Keep answers short, friendly and supportive."""
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                })
            )

            print("STATUS CODE:", response.status_code)
            print("RESPONSE:", response.text)

            result = response.json()

            if 'choices' in result:
                answer = result['choices'][0]['message']['content']
                return JsonResponse({'answer': answer})
            elif 'error' in result:
                print("API ERROR:", result['error'])
                return JsonResponse({'answer': f"API Error: {result['error'].get('message', 'Unknown error')}"})
            else:
                print("UNEXPECTED RESPONSE:", result)
                return JsonResponse({'answer': 'Unexpected response from AI. Please try again.'})

        except Exception as e:
            print("EXCEPTION:", str(e))
            return JsonResponse({'answer': f'Error: {str(e)}'})

    return JsonResponse({'error': 'Invalid request'}, status=400)