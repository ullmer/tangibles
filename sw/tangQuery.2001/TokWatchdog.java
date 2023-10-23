// Token Watchdog
// By Brygg Ullmer, MIT Media Lab

// Begun October 9, 2001

import java.util.*;
import java.io.*;

//////////////////////////////////////////////////////
///////////////// Token Watchdog /////////////////////
//////////////////////////////////////////////////////


public class TokWatchdog {

//////////////////// members /////////////////////

  //int   leaseTime = 750; // n milliseconds of "lease"
  //int   leaseTime = 1000; // n milliseconds of "lease"

  int   leaseTime = 1500; // n milliseconds of "lease"
                           // more "stability?"

  long  lastSeen    = -1;
  long  currentTime = -1;

  boolean active = false;

//////////////////// methods /////////////////////

//  public void    tokWitnessed();
//  public boolean isTokActive();

/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

///////////// constructor ///////////////

  public TokWatchdog() {
  }

///////////// tokWitnessed ///////////////

  public void tokWitnessed() {

    lastSeen = System.currentTimeMillis();
    active = true;
  }

///////////// isTokActive ///////////////

  public boolean isTokActive() {

    currentTime = System.currentTimeMillis();

    if (lastSeen == -1 || active == false) {
      return false;
    }

    long diff = currentTime - lastSeen;

    if (diff < leaseTime) { 
      return true;
    } else {
      active = false;
      return false;
    }
  }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("TokWatchdog[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
