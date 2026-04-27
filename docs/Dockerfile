FROM jekyll/minimal

RUN gem install jekyll-remote-theme webrick

COPY docs/ /srv/jekyll/
COPY README.md /tmp/README.md
COPY CONTRIBUTING.md /tmp/CONTRIBUTING.md

RUN printf -- '---\n---\n\n' > /srv/jekyll/index.md \
    && cat /tmp/README.md >> /srv/jekyll/index.md \
    && printf -- '---\ntitle: Contributing\n---\n\n' > /srv/jekyll/contributing.md \
    && cat /tmp/CONTRIBUTING.md >> /srv/jekyll/contributing.md

EXPOSE 4000

CMD ["jekyll", "serve", "--host", "0.0.0.0"]
