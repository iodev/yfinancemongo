#!/usr/bin/perl
open SYM, "Symbols.csv" or die; 
open LST, ".lastDownloadSym";
@lst = <LST>;
close LST;
chomp @lst;
$reachedLast = 0;
if(length(@lst) == 0){
  $reachedLast = 1;
}
$lastsym = $lst[0];
print "reachedLast=$reachedLast and lst[0] = $lst[0]\n";
while(<SYM>){ 
  @sym=split /\t/;
  chomp @sym;
  if(!$reachedLast){
    print "compare $sym[1] to $lastsym\n";
    if($sym[1] eq $lastsym){
      $reachedLast = 1;
      print "Reached lastsym $sym[1]\n";
    }
    next;
  }
  print "Querying for ".$sym[0]."\n"; 
  $result=`./quoteSummary.py $sym[1]`; 
  print $result;
  $lstSrch = $sym[1];
  `echo $lstSrch >.lastDownloadSym`;
  sleep(5); 
}

