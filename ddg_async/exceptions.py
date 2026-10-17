class DDGError(Exception):
    """Базовый класс для всех ошибок библиотеки."""
    pass

class DDGTokenError(DDGError):
    """Выбрасывается, когда не удалось получить защитный токен vqd."""
    pass