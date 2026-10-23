FROM ruby:alpine
RUN apk add --update build-base curl \
 && addgroup -S app && adduser -S app -G app \
 && mkdir -p /app \
 && chown -R app:app /app
WORKDIR /app
# Install gems as root so they are available system-wide
RUN gem install sinatra -v "~> 2.2" \
 && gem install thin
USER app
ADD hasher.rb /app/
CMD ["ruby", "hasher.rb"]
EXPOSE 8080
