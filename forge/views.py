import json
from django.shortcuts import render
from django.http import JsonResponse
from groq import Groq

CONTENT_TYPES = {
    'story': {
        'label': 'Short Story',
        'emoji': '📖',
        'system': 'You are a masterful fiction writer. Write vivid, emotionally resonant short stories with strong characters and unexpected twists.',
        'prompt_template': 'Write a compelling short story about: {topic}. Tone: {tone}. Keep it under 400 words but make every word count.',
    },
    'blog': {
        'label': 'Blog Post',
        'emoji': '✍️',
        'system': 'You are an engaging blogger who writes with personality and insight. Your posts are witty, well-structured, and leave readers thinking.',
        'prompt_template': 'Write an engaging blog post about: {topic}. Tone: {tone}. Include a catchy title (marked with #), an intro hook, 2-3 key points, and a memorable conclusion. Around 300 words.',
    },
    'poem': {
        'label': 'Poem',
        'emoji': '🎭',
        'system': 'You are a poet with a gift for imagery and rhythm. Write poetry that surprises, moves, and lingers in the mind.',
        'prompt_template': 'Write a poem about: {topic}. Tone: {tone}. Be evocative and original — avoid clichés.',
    },
    'tweet_thread': {
        'label': 'Tweet Thread',
        'emoji': '🐦',
        'system': 'You are a viral content creator who writes punchy, shareable tweet threads. Each tweet hooks the reader into the next.',
        'prompt_template': 'Write a 5-tweet thread about: {topic}. Tone: {tone}. Number each tweet (1/5, 2/5, etc.). Make it shareable and engaging.',
    },
    'script': {
        'label': 'Micro Script',
        'emoji': '🎬',
        'system': 'You are a screenwriter who crafts tight, punchy dialogue-driven scenes. Every line reveals character.',
        'prompt_template': 'Write a short script scene about: {topic}. Tone: {tone}. Include character names, dialogue, and brief stage directions. Keep it under 300 words.',
    },
}

TONES = ['Inspiring', 'Humorous', 'Dark & Gritty', 'Whimsical', 'Suspenseful', 'Romantic', 'Satirical', 'Nostalgic']

MODELS = [
    ('llama-3.3-70b-versatile', 'Llama 3.3 70B — Most Creative'),
    ('llama-3.1-8b-instant', 'Llama 3.1 8B — Fastest'),
    ('gemma2-9b-it', 'Gemma 2 9B — Balanced'),
]

def index(request):
    return render(request, 'forge/index.html', {
        'content_types': CONTENT_TYPES,
        'tones': TONES,
        'models': MODELS,
    })

def generate(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
        topic = data.get('topic', '').strip()
        content_type = data.get('content_type', 'story')
        tone = data.get('tone', 'Inspiring')
        model = data.get('model', 'llama-3.3-70b-versatile')
        api_key = data.get('api_key', '').strip()

        if not topic:
            return JsonResponse({'error': 'Please enter a topic.'}, status=400)
        if not api_key:
            return JsonResponse({'error': 'Please enter your Groq API key.'}, status=400)
        if content_type not in CONTENT_TYPES:
            return JsonResponse({'error': 'Invalid content type.'}, status=400)

        ct = CONTENT_TYPES[content_type]
        prompt = ct['prompt_template'].format(topic=topic, tone=tone)

        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': ct['system']},
                {'role': 'user', 'content': prompt},
            ],
            temperature=0.9,
            max_tokens=800,
        )

        content = completion.choices[0].message.content
        usage = completion.usage

        return JsonResponse({
            'content': content,
            'model': model,
            'tokens': usage.total_tokens if usage else None,
            'content_type': ct['label'],
            'emoji': ct['emoji'],
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
