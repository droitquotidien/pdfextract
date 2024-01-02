.PHONY: text2md

build-text2md: build-docker
	make text2md file=$(file)

text2md:
	docker run -v ./exemples:/data -it pdftools /venvs/pdftools/bin/text2md /data/$(file) /data/$(basename $(file)).md

build-text2md-all: build-docker
	@for file in exemples/*.txt; do \
		make text2md file=$${file#exemples/}; \
	done

build-docker:
	docker build -t pdftools .
