import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course):
    """Создает продукт stripe"""
    return stripe.Product.create(name=course.name)


def create_stripe_price(product, amount):
    """Создает цену stripe"""
    return stripe.Price.create(
        product=product.get("id"),
        currency="rub",
        unit_amount=int(amount) * 100,
    )


def create_stripe_session(price):
    """Создавет сессию stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/courses/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def check_status_stripe(session_id):
    """Проверяет статус оплаты"""
    return stripe.checkout.Session.retrieve(session_id)
