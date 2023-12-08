import yaml

yfn='index.yaml'
yf = open(yfn, 'rt')
yd = yaml.safe_load(yf)
print(yd)

