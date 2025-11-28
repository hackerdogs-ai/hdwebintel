

class webpagemodel:

  
  def __init__(self, url, fqdn=None, domain=None, registered_domain=None, subdomain=None, suffix=None, ip_locations=None, language=None, text_content=None, entities=None, title=None, description=None, keywords=None, emails=None, email_domains=None, ip_locations_fqdn=None, whois=None, phones=None, bag_of_terms=None, readability_stats=None, timestamp=None, links=None):
    self.ip_locations = ip_locations
    self.fqdn = fqdn
    self.domain = domain
    self.subdomain = subdomain
    self.suffix = suffix
    self.language = language
    self.text_content = text_content
    self.url = url
    self.entities = entities
    self.title = title
    self.description = description
    self.keywords = keywords
    self.emails = emails
    self.email_domains = email_domains
    self.ip_locations_fqdn = ip_locations_fqdn
    self.registered_domain = registered_domain
    self.whois = whois
    self.phones = phones
    self.bag_of_terms = bag_of_terms
    self.readability_stats = readability_stats
    self.timestamp = timestamp
    self.links = links
    #self.credit_cards = credit_cards
    
    
 
