import yaml
yfn = 'cspTagAkaMin01.yaml'
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)
print(yd)
