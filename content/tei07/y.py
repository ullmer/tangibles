import yaml

yfn='content.yaml'
yf = open(yfn, 'rt')
yd = yaml.safe_load(yf)
print(yd)

