from django.conf import settings


class AIService:
    """Claude-powered AI services for Fizi.uz."""

    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def generate_listing_description(self, title: str, category: str, condition: str) -> str:
        """Generate a compelling listing description."""
        message = self.client.messages.create(
            model='claude-3-5-haiku-20241022',
            max_tokens=500,
            messages=[{
                'role': 'user',
                'content': (
                    f"Напиши привлекательное описание для объявления на сайте объявлений Fizi.uz.\n"
                    f"Название: {title}\n"
                    f"Категория: {category}\n"
                    f"Состояние: {condition}\n"
                    f"Описание должно быть на русском языке, 2-3 предложения."
                )
            }]
        )
        return message.content[0].text

    def moderate_listing(self, title: str, description: str) -> dict:
        """Check listing content for policy violations."""
        message = self.client.messages.create(
            model='claude-3-5-haiku-20241022',
            max_tokens=200,
            messages=[{
                'role': 'user',
                'content': (
                    f"Проверь это объявление на нарушения правил маркетплейса.\n"
                    f"Заголовок: {title}\n"
                    f"Описание: {description}\n"
                    f"Ответь в формате JSON: {{\"ok\": true/false, \"reason\": \"...\"}}"
                )
            }]
        )
        import json
        try:
            return json.loads(message.content[0].text)
        except Exception:
            return {'ok': True, 'reason': ''}

    def suggest_category(self, title: str, description: str) -> str:
        """Suggest the most appropriate category slug."""
        message = self.client.messages.create(
            model='claude-3-5-haiku-20241022',
            max_tokens=50,
            messages=[{
                'role': 'user',
                'content': (
                    f"Для объявления определи категорию (верни только slug на английском).\n"
                    f"Заголовок: {title}\n"
                    f"Описание: {description}"
                )
            }]
        )
        return message.content[0].text.strip()
