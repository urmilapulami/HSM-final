from django.shortcuts import render
from django.http import JsonResponse
from django_dump_die.middleware import dump

import openai

# Set your OpenAI API key (replace 'YOUR_OPENAI_API_KEY' with your actual key)
# openai.api_key = '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'
# from openai

# client = OpenAI()
# Set your OpenAI API key (replace 'YOUR_OPENAI_API_KEY' with your actual key)
# openai.api_key = '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'
openai.api_key = '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'


prefix='frontend/pages/'
def dashboard(request):
    return render(request,prefix+'home.html', {})

def chat(request):
    if request.method == 'POST':
        
        user_input = request.POST.get('message', '')
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=user_input,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7,
            top_p=None,
            frequency_penalty=None,
            presence_penalty=None
        )

        chat_response = response.choices[0].text.strip()

        return JsonResponse({'reply': chat_response})

    return JsonResponse({'reply': 'Invalid request'})

