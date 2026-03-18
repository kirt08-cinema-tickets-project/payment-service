FROM python:3.12.3-slim

WORKDIR /app

# гарантирует, что мы сможем видеть выходные данные в режими реального времени
ENV PYTHONUNBUFFERED=1 

# отключает создание файлов .pyc, в которых храниться байт код
ENV PYTHONDONTWRITEBYTECODE=1

ENV POETRY_VERSION=2.2.1
ENV POETRY_HOME="/opt/poetry" 

# при инициализации, поетри создает виртуальное окржение. Зачем нам оболочка внутри оболочки? - Отключаем
ENV POETRY_VIRTUALENVS_CREATE=false

ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_NO_INTERACTION=1 

# ENV PYSETUP_PATH="/opt/pysetup"

RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential

RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . .

ENV ENVIRONMENT=production

CMD ["python", "-m", "src.core.main"]
