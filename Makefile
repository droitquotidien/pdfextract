.PHONY: text2md

pdf2text-all:
	@for file in exemples/*.pdf; do \
		make pdf2text file=$${file#exemples/}; \
	done

pdf2text:
	docker run -v ./exemples:/data -it pdftools /usr/bin/pdftotext -layout /data/$(file)

build-text2md: build-docker
	make text2md file=$(file)

build-text2md-all: build-docker
	@for file in exemples/*.txt; do \
		make text2md file=$${file#exemples/}; \
	done

text2md:
	docker run -v ./exemples:/data -it pdftools /venvs/pdftools/bin/text2md /data/$(file) /data/$(basename $(file)).md

build-md2xml: build-docker
	make md2xml file=$(file)

build-md2xml-all: build-docker
	@for file in exemples/*.md; do \
		make md2xml file=$${file#exemples/}; \
	done

md2xml:
	docker run -v ./exemples:/data -it pdftools /venvs/pdftools/bin/md2xml /data/$(file) /data/$(basename $(file)).xml

build-docker:
	docker build -t pdftools .
