package ContentGenerator;
use XML::LibXML;

$singleAction = "
<BES>
    <SingleAction>
        <Title></Title>
        <ActionScript MIMEType=\"application/x-Fixlet-Windows-Shell\">
        </ActionScript>
        <!-- Set to CustomRelevance for custom success criteria -->
        <SuccessCriteria Option=\"RunToCompletion\"></SuccessCriteria>
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
            <PostActionBehavior Behavior=\"Nothing\"></PostActionBehavior>
            <IsOffer>false</IsOffer>
        </Settings>
        <IsUrgent>false</IsUrgent>
    </SingleAction>
</BES>
";
sub createAction{
    my($title, $relevance, $action) = @_;
    $dom = XML::LibXML->load_xml(string => $singleAction);
    @sa = $dom->getElementsByTagName("SingleAction");
    (@sa[0]->getElementsByTagName("Title"))[0]->appendText($title);
    foreach(@$relevance){
        $node = XML::LibXML::Element->new("Relevance");
        $node->appendText($_);
        @sa[0]->addChild($node);
    }
    @as = @sa[0]->getElementsByTagName("ActionScript");
    foreach(@$action){
        @as[0]->appendText($_."\n");
    }
    print $dom;
}
