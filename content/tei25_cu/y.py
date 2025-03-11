import yaml
yfn = 'gpc.yaml'
#yfn = 'g02.yaml'
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)

print(yd)
