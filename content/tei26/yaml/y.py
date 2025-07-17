import yaml
yfn='physDescrReeds.yaml'
yf =open(yfn, 'rt')
yd =yaml.safe_load(yf)
print(yd)
