import numpy as np
import pandas as pd
import os

from database import Database
from flask import current_app

from assignments import Assignment


def drawing(particip, couples):
	
	participants = {}
	#convert values to str
	for participant_key, participant in particip:
		participants[participant.participant] = participant.email

	# print(participants)
	
	# this will keep trying until the conditions are met (break).
	while True:
		# randomize list of names
		gift_giver = list(np.random.choice(list(participants.keys()), len(list(participants.keys())), replace = False))
		# offset list of receivers by one. this way no one can get their own name
		gift_receiver = []
		for k in range(-1, len(gift_giver)-1):
			gift_receiver.append(gift_giver[k])

		# create dict from gift_givers receivers to show pairs
		assignment_dict = dict(zip(gift_giver, gift_receiver))

		# break # temporary break

		##################################### COUPLES #####################################

		couples_dict = {}
		#convert values to str
		for couple_key, couple in couples:
			couples_dict[couple.partner_one] = couple.partner_two

		# print(couples_dict)

		# create a list that will be full of pass/fail. want it to be all passes. if not, infinite loop will continue (no break)
		list_of_pass_or_fail = []

		# test if the pairs work. fill out list_of_pass_or_fail list with pass/fail
		for partner1, partner2 in couples_dict.items():
			for name1, name2 in assignment_dict.items():
				print(partner1, name1)
				print(partner2, name2)
				if str(partner1) == str(name1) and str(partner2) == str(name2) or str(partner2) == str(name1) and str(partner1) == str(name2):
					# print('Problem! ' + str(partner1) + ' and ' + str(partner2[0]) + ' cannot match!')
					list_of_pass_or_fail.append('fail')
				else:
					list_of_pass_or_fail.append('pass')

		# create a passing list with the same length as the list_of_pass_or_fail list
		passing_list = []
		count = 0
		while count < len(list_of_pass_or_fail):
			passing_list.append('pass')
			count += 1

		print(list_of_pass_or_fail)

		# compare perfect list to the list_of_pass_or_fail list. if it matches, break the loop
		if list_of_pass_or_fail == passing_list:
			break


		##################################### COUPLES #####################################


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
		print(name1)
		print(type(name1))
		db.add_assignment(Assignment(str(name1), str(name2)))


	print(db.get_assignments())
	return db.get_assignments()


