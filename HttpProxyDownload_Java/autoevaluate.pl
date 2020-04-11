#! /usr/bin/perl 
# You may need to modify this ^^ based on your platform and location of the perl binary

if ($#ARGV != 0)
{
	print "Requires filename as argument\n";
	exit(0);
}

my $file, $i, $flag = 0, $j=0;
my @emails, @names;

open($file, "<", $ARGV[0]) or die $!;

@lines = <$file>;

for $i(0..$#lines)
{
	$lines[$i] =~ s/^\s+|\s+$//g;
	if($lines[$i] eq "/* BeginGroupMembers */")
	{
		$flag = 1;
		next;
	}
	if($lines[$i] eq "/* EndGroupMembers */")
	{
		$flag = 2;
		next;
	}
	
	if ($flag == 1)
	{
		$lines[$i] =~ m/\/\*\s+(.*?)\s+(.*)\s+\*\//;
		$emails[$j] = $1;
		$names[$j++] = $2;
	}
}
close($file);

for $i(0..$#emails)
{
	print "Group Member $i: Name: |$names[$i]| Email: |$emails[$i]|\n";
}
