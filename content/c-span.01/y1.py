import yaml
yfn='cspan-tags.yaml'
yf =open(yfn, 'rt')
yd =yaml.safe_load(yf)
print(yd)
