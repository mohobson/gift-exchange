import numpy as np
import pandas as pd
import os

from database import Database
from flask import current_app


def drawing(particip):
	fileName = 'participants.xlsx'
	# df = pd.read_excel(fileName, sheet_name = "participants")

	# particip = df.set_index('name').T.to_dict('list')

	participants = {}
	#convert values to str
	for participant_key, participant in particip:
		# print(participant_key)
		# print(participant.participant)
		# print(participant.email)
		participants[participant.participant] = participant.email

	print(participants)
	
	# this will keep trying until the conditions are met (break).
	while True:
		# randomize list of names
		santa = list(np.random.choice(list(participants.keys()), len(list(participants.keys())), replace = False))
		# offset list of receivers by one. this way no one can get their own name
		recvr = []
		for k in range(-1, len(santa)-1):
			recvr.append(santa[k])

		# create dict from santas receivers to show pairs
		assignment_dict = dict(zip(santa, recvr))

		break # temporary break

		# for adding COUPLES ################
		#####################################

		# df2 = pd.read_excel(fileName, sheet_name = "couples")

		# couples = df2.set_index('partner1').T.to_dict('list')

		# # create a list that will be full of pass/fail. want it to be all passes. if not, infinite loop will continue (no break)
		# token = []

		# # test if the pairs work. fill out token list with pass/fail
		# for partner1, partner2 in couples.items():
		# 	for key, value in dictionary.items():
		# 		if str(partner1) == str(key) and str(partner2[0]) == str(value) or str(partner2[0]) == str(key) and str(partner1) == str(value):
		# 			# print('Problem! ' + str(partner1) + ' and ' + str(partner2[0]) + ' cannot match!')
		# 			token.append('fail')
		# 		else:
		# 			token.append('pass')

		# # create a passing list with the same length as the token list
		# passing_list = []
		# count = 0
		# while count < len(token):
		# 	passing_list.append('pass')
		# 	count += 1

		# # compare perfect list to the token list. if it matches, break the loop
		# if token == passing_list:
		# 	break


		#####################################


	# from dotenv import load_dotenv
	# load_dotenv()

	# send emails
	# import grid
	# fromaddr = os.environ.get('fromaddr')
	# subject = 'Gift Exchange Time'



	# for member, addr in participants.items():
	# 	name = dictionary[member]
	# 	print(member, name)
		# grid.sendgrid_email(addr, fromaddr, subject, name)
	print(assignment_dict)
	db = current_app.config["db"]

	for name1, name2 in assignment_dict.items():
		db.add_assignment(name1, name2)

	print(db.get_assignments())
	return db.get_assignments()


