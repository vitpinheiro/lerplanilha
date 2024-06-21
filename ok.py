import pandas as pd

d= {'Nome':['Ana', 'Joao', 'Maria'], 'Idade': [20, 45,38]}

dados = pd.DataFrame(data=d)
print(dados)

dados.to_excel('dados.xlsx', index= False)