class DefaultValue:
    def template_title_value(self, context: dict) -> dict:
        context['title'] = 'Страница книг'
        return context