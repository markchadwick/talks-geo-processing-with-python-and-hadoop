# -----------------------------------------------------------------------------
# Britekite data sets

SAMPLE_SIZE = 10000

data/britekite.all.tsv:
	curl http://snap.stanford.edu/data/loc-brightkite_totalCheckins.txt.gz | gzip -d > data/britekite.all.tsv

data/britekite.shuffled.tsv: data/britekite.all.tsv
	sort -R -o data/britekite.shuffled.tsv data/britekite.all.tsv

data/britekite.sample.tsv: data/britekite.shuffled.tsv
	head -$(SAMPLE_SIZE) data/britekite.shuffled.tsv > data/britekite.sample.tsv

# -----------------------------------------------------------------------------
# Jobs

JOB_INPUT = data/britekite.sample.tsv

out/user_playgrounds: $(JOB_INPUT)
	python user_playgrounds.py $(JOB_INPUT) | sort -rn > out/user_playgrounds

out/top5.geojson: out/user_playgrounds
	python top.py 5 < out/user_playgrounds > out/top5.geojson

clean:
	rm -rf out/*

all: out/top5.geojson
