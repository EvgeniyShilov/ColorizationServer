#!/usr/bin/python

from gcm import GCM

def notify(id, token):
	gcm = GCM("AIzaSyBk6qJ9tIij0GCezqDUfGu-IekXmbayE2k")
	data = {'id': id}
	gcm.plaintext_request(registration_id=token, data=data)
