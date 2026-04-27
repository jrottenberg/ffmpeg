FROM jekyll/minimal

RUN gem install jekyll-remote-theme webrick

COPY docs/ /srv/jekyll/
COPY README.md /tmp/README.md

RUN printf -- '---\n---\n\n' > /srv/jekyll/index.md \
    && cat /tmp/README.md >> /srv/jekyll/index.md

EXPOSE 4000

CMD ["jekyll", "serve", "--host", "0.0.0.0"]
