import pandas as pd
from app.models import Product
from app import db

def import_pb():
	# open the file
	try:
		# xlsx = pd.ExcelFile('pricebook.xlsx')
		pricebook_nan = pd.read_excel('pricebook.xlsx')
	except:
		print("didn't open the file, make sure correct name")
		exit(1)

	# convert nans to Nones for mysql
	pricebook = pricebook_nan.where((pd.notnull(pricebook_nan)), None)

	for row in range(0,len(pricebook.index)):
		p_id = pricebook['ProductID'][row]	
		p_number = pricebook['Part Number'][row]	         
		p_name = pricebook['ProductName'][row]	
		unit_price = pricebook['UnitPrice'][row]	
		p_note = pricebook['Product Note to show'][row]	
		cost_native = pricebook['Cost Native'][row]	
		exchange_rate = pricebook['Exchange Rate used'][row]	
		unit_cost = pricebook['Unit Cost'][row]	
		supplier = pricebook['Supplier'][row]	
		p_category = pricebook['Product Category'][row]	
		p_status = pricebook['Product Status'][row]	
		date_created = pricebook['Date Created'][row]	
		# person_created = pricebook['Person Created'][row]	
		remarks = pricebook['Remarks'][row]	
		japanese_p_name = pricebook['Japanese ProductName'][row]	
		japanese_unit_price = pricebook['Japanese UnitPrice'][row]
		japanese_note = pricebook['Product Note to show - Japanese'][row]	

		product = Product(p_number=p_number,
							p_name=p_name,
							unit_price=unit_price,
							p_note=p_note,
							cost_native=cost_native,
							exchange_rate=exchange_rate,
							unit_cost=unit_cost,
							supplier=supplier,
							p_category=p_category,
							p_status=p_status,
							date_created=date_created,
							remarks=remarks,
							japanese_p_name=japanese_p_name,
							japanese_unit_price=japanese_unit_price,
							japanese_note=japanese_note)

		try:
			db.session.add(product)
			db.session.commit()
			print 'added row ' + str(row)
		except Exception as e:
			print(e)
			print 'skipping ' + str(row)
			db.session.rollback()
			continue
	print 'done'


if __name__ == '__main__':
	import_pb()

