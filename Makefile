GENEI_MONO_GOTHIC_VERSION := 1.0
JET_BRAINS_MONO_VERSION := 2.304

SOURCES := \
	fonts/GenEiMonoGothic-Regular.ttf \
	fonts/GenEiMonoGothic-Bold.ttf \
	fonts/JetBrainsMono-Regular.ttf \
	fonts/JetBrainsMono-Italic.ttf \
	fonts/JetBrainsMono-Bold.ttf \
	fonts/JetBrainsMono-BoldItalic.ttf

FONTS := \
	dist/MomiageMonoNerdFont-Regular.ttf \
	dist/MomiageMonoNerdFont-Italic.ttf \
	dist/MomiageMonoNerdFont-Bold.ttf \
	dist/MomiageMonoNerdFont-BoldItalic.ttf

ZIP := dist/MomiageMono-$(shell date '+%Y%m%d').zip

all: fonts dist $(ZIP)
	unzip -l $(ZIP)

$(ZIP): $(FONTS)
	zip -T -j $@ dist/*.ttf ./LICENSE

fonts dist:
	$(RM) -r $@
	mkdir -p $@

fonts/GenEiMonoGothic_v$(GENEI_MONO_GOTHIC_VERSION).zip:
	curl -Ss -f -o $@ -L --compressed https://okoneya.jp/font/$(@F)

fonts/JetBrainsMono-$(JET_BRAINS_MONO_VERSION).zip:
	curl -Ss -f -o $@ -L https://github.com/JetBrains/JetBrainsMono/releases/download/v$(JET_BRAINS_MONO_VERSION)/$(@F)

fonts/GenEiMonoGothic-%.ttf: fonts/GenEiMonoGothic_v$(GENEI_MONO_GOTHIC_VERSION).zip
	unzip -d $(@D) -j $^ $(basename $(^F))/GenEiMonoGothic-$*.ttf

fonts/JetBrainsMono-%.ttf: fonts/JetBrainsMono-$(JET_BRAINS_MONO_VERSION).zip
	unzip -d $(@D) -j $^ fonts/ttf/JetBrainsMono-$*.ttf

dist/MomiageMono-%.ttf: $(SOURCES)
	./scripts/momiage-mono.py $(@F)

dist/MomiageMonoNerdFont-%.ttf: dist/MomiageMono-%.ttf
	./nerd-fonts/font-patcher -c -q -out ./dist $< 2>/dev/null

clean:
	$(RM) -r dist fonts

.PHONY: all clean
