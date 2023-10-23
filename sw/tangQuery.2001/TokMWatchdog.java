// Token meta-Watchdog -- modified
// By Brygg Ullmer, MIT Media Lab

// Begun October 9, 2001

import java.util.*;
import java.io.*;

//////////////////////////////////////////////////////
///////////////// Token Watchdog /////////////////////
//////////////////////////////////////////////////////

// Meta-watchdog / modified-Watchdog
// reed switch gives us entrance and exit event, but we don't
// want to interpret the exit event if another entrance arrives within
// n time units.  Modify the logic of this function correspondingly...


public class TokMWatchdog {

//////////////////// members /////////////////////

  //int   leaseTime = 750; // n milliseconds of "lease"
  //int   leaseTime = 1000; // n milliseconds of "lease"
//  int   leaseTime = 500; // n milliseconds of "lease"


  int   leaseTime = 10; // n milliseconds of "lease"
// almost = turning off this feature

  long  lastUpdate    = -1;
  long  currentTime = -1;

  int lastClaim = 0;

  boolean active = false;

//////////////////// methods /////////////////////

//  public void    tokWitnessed();
//  public boolean isTokActive();

/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

///////////// constructor ///////////////

  public TokMWatchdog() {
  }

///////////// tokWitnessed ///////////////

  public void tokWitnessed() {

    lastUpdate = System.currentTimeMillis();

    active = true;
    lastClaim = 1;
  }

///////////// tokClaimsDeparture ///////////////

  public void tokClaimsDeparture() {

    lastUpdate = System.currentTimeMillis();
    lastClaim = 0;
  }

///////////// isTokPresent ///////////////

  public boolean isTokPresent() {

    currentTime = System.currentTimeMillis();

    if (lastClaim == 0 && (lastUpdate == -1 || active == false)) {
      return false;
    }

    long diff = currentTime - lastUpdate;

    if (diff < leaseTime || lastClaim == 1) { 
      return true;
    } else {
      active = false;
      return false;
    }
  }

  public boolean isTokActive() {
    return isTokPresent();
  }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("TokMWatchdog[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
