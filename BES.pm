package BES;

use strict;
use warnings;

use XML::LibXML;

sub parseXML {
    my $file = $_[0];

    my $parser = XML::LibXML->new();
    my $xml = $parser->parse_file($file);

    my @bes = ();
    foreach my $fixletNode ($xml->findnodes('/BES/Fixlet')) {
        my $fixlet = {
            'Title' => $fixletNode->findnodes('./Title')->to_literal,
            'Description' => $fixletNode->findnodes('./Description')->to_literal,
            'Relevances' => []
        };

        foreach my $relevanceNode ($fixletNode->findnodes('./Relevance')) {
            $fixletNode->removeChild($relevanceNode);
            push($fixlet->{'Relevances'}, ($relevanceNode->to_literal));
        }

        foreach my $child ($fixletNode->getChildnodes()) {
            $fixlet->{$child->getName()} = $child->to_literal;
        }


        push(@bes, $fixlet);
    }

    return @bes;
}

return 1;