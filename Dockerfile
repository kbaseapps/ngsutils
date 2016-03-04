FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update

# -----------------------------------------


WORKDIR /kb/module

# Install ngsutils
RUN \
  git clone https://github.com/ngsutils/ngsutils && \
  cd ngsutils && \
  git checkout tags/ngsutils-0.5.7 && \
  make

ENV PATH /kb/module/ngsutils/bin:$PATH

COPY ./ /kb/module
RUN mkdir -p /kb/module/work

RUN make

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
