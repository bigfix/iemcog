from xml.etree import ElementTree as ET

single_action = """
<BES>
    <SingleAction>
        <Title></Title>
        <Relevance></Relevance>
        <ActionScript MIMEType="application/x-Fixlet-Windows-Shell"></ActionScript>
        <!-- Set to CustomRelevance for custom success criteria -->
        <SuccessCriteria Option="RunToCompletion"></SuccessCriteria>
        <SecureParameter></SecureParameter>
        <Settings>
            <ActionUITitle />
            <PreActionShowUI>false</PreActionShowUI>
            <HasRunningMessage>false</HasRunningMessage>
            <RunningMessage><Text /></RunningMessage>
            <HasTimeRange>false</HasTimeRange>
            <HasStartTime>false</HasStartTime>
            <HasEndTime>true</HasEndTime>
            <EndDateTimeOffset>P1DT23H59M48S</EndDateTimeOffset>
            <HasDayOfWeekConstraint>false</HasDayOfWeekConstraint>
            <ActiveUserRequirement>NoRequirement</ActiveUserRequirement>
            <ActiveUserType>AllUsers</ActiveUserType>
            <HasWhose>false</HasWhose>
            <Reapply>false</Reapply>
            <HasReapplyLimit>false</HasReapplyLimit>
            <HasReapplyInterval>false</HasReapplyInterval>
            <HasRetry>false</HasRetry>
            <HasTemporalDistribution>false</HasTemporalDistribution>
            <ContinueOnErrors>true</ContinueOnErrors>
            <PostActionBehavior Behavior="Nothing"></PostActionBehavior>
            <IsOffer>false</IsOffer>
        </Settings>
        <IsUrgent>false</IsUrgent>
    </SingleAction>
</BES>
"""

def createAction(title, relevance, action, computerIDs, secureParameters, skipUI, openDocuments, customSiteName):
    t = ET.ElementTree(ET.fromstring(single_action))
    a = t.getroot()[0]
    node = a.find("Title")
    node.text = title
    #t.getroot()[0][0].text = "My Fixlet"
    
    #node.text = "test"
    """
			ActionXML.SingleAction.Title = Title.replace(/\\/g, "\\\\");
			ActionXML.SingleAction.Relevance = Relevance.join(" AND ").replace(/\\/g, "\\\\");
			ActionXML.SingleAction.ActionScript = Action.join("\n").replace(/\\/g, "\\\\");

			if(SecureParameters){
				var i:int = 0;
				for(var key:String in SecureParameters){
					ActionXML[0].SingleAction.SecureParameter[i] = <SecureParameter Name={key}>{SecureParameters[key].replace(/\\/g, "\\\\")}</SecureParameter>;
					i++;
				}
			}else{
				delete ActionXML.SingleAction.SecureParameter;
			}
			
			if(skipUI){
				ActionXML['@SkipUI'] = 'true';
				if(computerIds){
					if(SecureParameters || GilmanCheck(computerIds)){
						ActionXML.SingleAction.appendChild(<Target></Target>);
						for each(var computerId:int in computerIds){
							ActionXML.SingleAction.Target.appendChild(<ComputerID>{computerId}</ComputerID>);
						}
					}else{
						ActionXML.SingleAction.Relevance += ' AND (computer id = ' + computerIds.join(' OR computer id = ') + ')';
					}
				}
			}else{
				ActionXML['@SkipUI'] = 'false';
			}
			
			BFExternalInterface.callWithCallback("ImportXMLRequest", resultsCallback, "requestImport", ActionXML.toString(), true, openDocuments, customSiteName, computerIds);
            """
    t.write("page1.xhtml")