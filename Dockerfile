# Documentation hosting (mkdocs build + hosting via nginx)
# Commands:
#   - Build image: docker build -t daemonizer-docs:latest .
#   - Create new container: docker run -d -p 8001:80 --name daemonizer-docs daemonizer-docs:latest

FROM ghcr.io/astral-sh/uv:alpine AS build

ENV UV_PYTHON=3.13
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app/src

ENV TZ=Europe/Zurich

WORKDIR /app

RUN apk add --no-cache git

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-default-groups --only-group docs

COPY . .

RUN uv run --no-project mkdocs build # --strict

FROM nginx:alpine AS prod

COPY --from=build /app/site /usr/share/nginx/html

COPY docs/static/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
