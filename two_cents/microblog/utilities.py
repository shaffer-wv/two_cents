import re

from django.db.models import Q

def normailize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def build_query(query_string, search_fields):

	query = None
	terms = normailize_query(query_string)
	for term in terms:
		or_query = None
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name: term})

			if or_query:
				or_query = or_query | q
			else:
				or_query = q

		if query:
			query = query & or_query
		else:
			query = or_query
	return query