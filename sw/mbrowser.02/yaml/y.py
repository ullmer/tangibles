import yaml
yfn='prismsAcmTei01.yaml'
yf = open(yfn, 'rt')
yd = yaml.safe_load(yf)
print(yd)
