import yaml
yfn = 'geomFRS05.yaml'
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)
print(yd)
