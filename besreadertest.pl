#/usr/bin/perl

use strict;
use warnings;

use BES;

my @bes = BES::parseXML('test/test.bes');
foreach my $fixlet (@bes) {
    print 'Title: '.$fixlet->{'Title'}."\n\n";
    foreach my $rel (@{$fixlet->{'Relevances'}}) {
        print 'Relevance: '.$rel."\n";
    }
}