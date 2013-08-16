from xml.etree import ElementTree as ET

fixlet = """
<BES>
	<Fixlet>
	</Fixlet>
</BES>
"""

fixletaction = """
<Action>
    <Description>
        <PreLink>Click </PreLink>
        <Link>here</Link>
        <PostLink></PostLink>
    </Description>
    <ActionScript MIMEType="application/x-Fixlet-Windows-Shell"></ActionScript>
</Action>
"""

def createFixlet(id, title, description, relevance, actions, parameters, MIMEfields):
    t = ET.ElementTree(ET.fromstring(fixlet))
    f = t.getroot()[0]
    
    node = ET.Element("Title")
    node.text = title
    f.append(node)
    
    node = ET.Element("Description")
    lines = ""
    for line in description:
        lines += line + "\n"
    node.text = lines
    f.append(node)

    for expression in relevance:
        node = ET.Element("Relevance")
        node.text = expression
        f.append(node)

    #parameters
    for (key, value) in parameters.items():
        node = ET.Element(key)
        node.text = value
        f.append(node)

    for MIME in MIMEfields:
        f.append(MIME)
        
    for action in actions:
        f.append(action)
    
    t.write(id + "-" + title + ".bes")
    
def createAction(ID, postLink, action):
    a = ET.fromstring(fixletaction)
    a.set('ID', ID)
    node = a.find("Description")
    node.find("PostLink").text = postLink
    node = a.find("ActionScript")
    lines = ""
    for line in action:
        lines += line + "\n"
    node.text = lines
    return a