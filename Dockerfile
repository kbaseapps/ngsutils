FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer

WORKDIR /kb/module

RUN pip install --upgrade ndg-httpsclient

# Install ngsutils
RUN \
  git clone https://github.com/ngsutils/ngsutils && \
  cd ngsutils && \
  git checkout tags/ngsutils-0.5.9 && \
  sed -i '/pysam/c\pysam==0.8.4' requirements.txt && \
  make

RUN \
  pip install -Iv requests_toolbelt>=0.7.0

ENV PATH /kb/module/ngsutils/bin:$PATH

COPY ./ /kb/module
RUN mkdir -p /kb/module/work

RUN make

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
