row1=['x','x','x']
row2=['x','x','x']
row3=['x','x','x']

matrix=[row1,row2,row3]

position=input('Enter a position you want to hide:')
row_number=int(position[0])
column_number=int(position[1])

row_selected=matrix[row_number-1]
row_selected[column_number-1]='@'

print(f'{row1}\n{row2}\n{row3}')

