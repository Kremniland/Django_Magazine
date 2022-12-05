class DefaultValue:
    def template_title_value(self, context: dict) -> dict:
        context['title'] = 'Страница книг'
        return context


def NDS(price, proc=0.10):
    return price * proc


def NDS_full(price, proc=0.10):
    return price + (price * proc)

