import re, requests
def getLinks(content, lined=False, link_patterns=[]):
    links = []
    match link_patterns:
        case []:
            link_patterns = ["https://", "http://"]
        case _:
            link_patterns.append("https://")
            link_patterns.append("http://")
    if lined:
        for line in content:
            segments = line.split(" ")
            for seg in segments:
                for pattern in link_patterns:
                    if re.search(pattern, seg):
                        m = re.split("\' |\"", seg)
                        if len(m) > 1:
                            links.append(m[1])
    # else:
    #     for pattern in link_patterns:
    #         if re.search(pattern, content):
    #             links.append(line)
    return links
def getHTML(link):
    HEADERS = { #NEEDS UPDATES OCCASIONALLY
        'Accept-Encoding'   : 'identity', # THIS LINE STAYS THE SAME
        'User-Agent'        : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0', # Firefox/xxx Will need to change depending on your version
        'Accept-Language'   : 'en-US,en;q=0.5',# THIS LINE STAYS THE SAME
        'Accept-Encoding'   : 'gzip, deflate',# THIS LINE STAYS THE SAME
        'Connection'        : 'keep-alive'# THIS LINE STAYS THE SAME
    }
    response = requests.get(link, headers=HEADERS)
    return response.text.split("\n")

def getHTMLLinks(link):
    return getLinks(getHTML(link), True)