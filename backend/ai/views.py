from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
import json


class AIListingSuggestView(APIView):
    """Suggest category and price based on listing title/description."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        title = request.data.get('title', '')
        description = request.data.get('description', '')

        if not getattr(settings, 'ANTHROPIC_API_KEY', ''):
            # Dev fallback
            return Response({
                'category_slug': 'electronics',
                'category_name': 'Электроника',
                'price_min': 500000,
                'price_max': 2000000,
                'currency': 'UZS',
            })

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            prompt = f"""Ты помощник маркетплейса в Узбекистане.
По объявлению определи категорию и диапазон цены в UZS.
Категории: electronics, auto, realty, clothing, home, jobs, services, animals, kids, sport, food, business

Название: {title}
Описание: {description}

Ответь ТОЛЬКО JSON: {{"category_slug":"...","category_name":"...","price_min":0,"price_max":0,"currency":"UZS"}}"""

            msg = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            text = msg.content[0].text.strip()
            start = text.find('{')
            end = text.rfind('}') + 1
            return Response(json.loads(text[start:end]))
        except Exception as e:
            return Response({'error': str(e)}, status=500)
