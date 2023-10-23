/// Query UI code 
/// By Brygg Ullmer, MIT Media Lab
/// Begun April 20, 2001
///
/// Based on threading template by Ben Fry (fry@media.mit.edu),
/// 4/18/2001, and WinHelp Java Tutorial: AnimatorApplication.java,
/// Arthur van Hoff

import java.util.*;
import java.io.*;

///////////////////////////////////////////////////////////
////////////////////  ReedTrans /////////////////////////////
///////////////////////////////////////////////////////////

public class ReedTrans {

// reed switch translator //


/////////////  methods ///////////////

// void registerTransition(int byteOrder, 
//                 String previous, String current, int whichCell, int whichPos)

// int assembleTransition(int byteOrder, int previousState, int currentState) 

//  public ReedStruct findTrans(int transition) 

// static void main(String args[])
// public ReedTrans()


/////////////  fields ///////////////

  public static final int HI_ORDER = 1;
  public static final int LO_ORDER = 0;

  Hashtable transitionHash = new Hashtable();
  Vector    transitionVect = new Vector();

  static public boolean verbose = true;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

///////////////////// register Transition ///////////////////////

  public void registerTransition(int byteOrder, 
                                        String previous, String current, 
		                        int whichPad, int whichPos) {

    int previousState = Integer.valueOf(previous, 2).intValue();
    int currentState  = Integer.valueOf(current,  2).intValue();

    int transition = (byteOrder << 8);
        transition |= (previousState << 4);
	transition |= currentState;

    ReedStruct struct = new ReedStruct();

    struct.byteOrder     = byteOrder;
    struct.previousState = previousState;
    struct.currentState  = currentState;
    struct.transition    = transition;

    struct.whichPad = whichPad;
    struct.whichPos = whichPos;

    transitionHash.put(new Integer(transition), struct);
    transitionVect.addElement(struct);
  }

///////////////////// assemble Transition /////////////////////

 public int assembleTransition(int byteOrder, int previousState, int currentState) {

   int current, prev;

   switch (byteOrder) {
     case HI_ORDER: 
       prev    = previousState; prev    &= 0xF0; 
       current = currentState;  current &= 0xF0; current >>= 4;
       break;

     case LO_ORDER:
       prev  =  previousState;  prev    &= 0xF; prev <<= 4;
       current =  currentState; current &= 0xF;
       break;

     default:
       dbg("Unhandled case in assembleTransition: bad byteOrder description!");
       return 0;
    }

    int transition = (byteOrder << 8);

    if (verbose) {dbg("TT: " + transition);}

    transition |= prev;
    transition |= current;

    if (verbose) {
      dbg("prev: " + Integer.toBinaryString(prev));
      dbg("current: " + Integer.toBinaryString(current));
      dbg("assembled transition " + transition + " (" + byteOrder + ")");
    }

    return transition;
 }

///////////////////// printTransitions ///////////////////////

  public ReedStruct findTrans(int transition) {

    Integer key = new Integer(transition);

    if (verbose) {
      dbg("findTrans called on val " + transition + " (" +
          Integer.toBinaryString(transition) + ")");
    }

    ReedStruct result = (ReedStruct) transitionHash.get(key);

    return result;

  }

///////////////////// printTransitions ///////////////////////

  void printTransitions() {

    int size = transitionVect.size();

    for (int i=0; i<size; i++) {
      ReedStruct struct = (ReedStruct) transitionVect.elementAt(i);
      struct.print();
    }
  }

////////////////////  construct /////////////////////////////

  public ReedTrans() {

  // FIRST PAD

    registerTransition(ReedTrans.LO_ORDER, "0100", "0110", 0, 0);

    registerTransition(ReedTrans.LO_ORDER, "0110", "0100", 0, 1);
    registerTransition(ReedTrans.LO_ORDER, "0010", "0100", 0, 1);

    registerTransition(ReedTrans.LO_ORDER, "0110", "0010", 0, 2);
    registerTransition(ReedTrans.LO_ORDER, "0100", "0010", 0, 2);

    registerTransition(ReedTrans.LO_ORDER, "0010", "0110", 0, 3);

  // SECOND PAD

    registerTransition(ReedTrans.HI_ORDER, "1101", "1110", 1, 4); 
    registerTransition(ReedTrans.HI_ORDER, "1111", "1110", 1, 4);  // relates to broken switch
    registerTransition(ReedTrans.HI_ORDER, "1100", "1110", 1, 4); 

    registerTransition(ReedTrans.HI_ORDER, "1110", "1101", 1, 5);
    registerTransition(ReedTrans.HI_ORDER, "1110", "1100", 1, 5); // broken switch

    registerTransition(ReedTrans.HI_ORDER, "1111", "1101", 1, 5);

    registerTransition(ReedTrans.HI_ORDER, "1101", "1111", 1, 6);
    registerTransition(ReedTrans.HI_ORDER, "0111", "1111", 1, 6);

    registerTransition(ReedTrans.HI_ORDER, "1111", "0111", 1, 7);

 // do we have another flakey reed switch?
    registerTransition(ReedTrans.HI_ORDER, "0101", "0110", 1, 4); 
    registerTransition(ReedTrans.HI_ORDER, "0111", "0110", 1, 4);  // relates to broken switch

    registerTransition(ReedTrans.HI_ORDER, "0110", "0101", 1, 5);
    registerTransition(ReedTrans.HI_ORDER, "0111", "0101", 1, 5);

    registerTransition(ReedTrans.HI_ORDER, "0101", "0111", 1, 6);

// this is getting quite strange...

    registerTransition(ReedTrans.HI_ORDER, "1101", "0101", 1, 7);
    registerTransition(ReedTrans.HI_ORDER, "0101", "1101", 1, 6);

    registerTransition(ReedTrans.HI_ORDER, "1101", "1100", 1, 4);


//    registerTransition(ReedTrans.HI_ORDER, "1011", "0111", 1, 4);

//    registerTransition(ReedTrans.HI_ORDER, "0111", "1011", 1, 5);

//    registerTransition(ReedTrans.HI_ORDER, "1011", "1111", 1, 6);
//    registerTransition(ReedTrans.HI_ORDER, "1110", "1111", 1, 6);



/*
// THIRD PAD

    registerTransition(ReedTrans.HI_ORDER, "1010", "0110", 2, 7);

    registerTransition(ReedTrans.HI_ORDER, "0110", "1010", 2, 6);
    registerTransition(ReedTrans.HI_ORDER, "1100", "1010", 2, 6);

    registerTransition(ReedTrans.HI_ORDER, "1010", "1100", 2, 5);
    registerTransition(ReedTrans.HI_ORDER, "1110", "1100", 2, 5);

    registerTransition(ReedTrans.HI_ORDER, "1100", "1110", 2, 4);


    registerTransition(ReedTrans.HI_ORDER, "0011", "0111", 2, 7);

    registerTransition(ReedTrans.HI_ORDER, "0111", "0011", 2, 6);
    registerTransition(ReedTrans.HI_ORDER, "0101", "0011", 2, 6);

    registerTransition(ReedTrans.HI_ORDER, "0011", "0101", 2, 5);
    registerTransition(ReedTrans.HI_ORDER, "0110", "0101", 2, 5);

    registerTransition(ReedTrans.HI_ORDER, "0101", "0110", 2, 4);


// FOURTH PAD

    registerTransition(ReedTrans.LO_ORDER, "0100", "0110", 3, 0);
    registerTransition(ReedTrans.LO_ORDER, "0100", "0110", 3, 0);

    registerTransition(ReedTrans.LO_ORDER, "0110", "0100", 3, 1);
    registerTransition(ReedTrans.LO_ORDER, "0010", "0100", 3, 1);

    registerTransition(ReedTrans.LO_ORDER, "0100", "0010", 3, 2);
*/


  }

////////////////////  Main /////////////////////////////

  static public void main(String args[]) {

    ReedTrans trans = new ReedTrans();

    trans.printTransitions();

  }

///////////////////// Debug ///////////////////////

  public static int dcnt;

  static public void dbg(String s) {

    System.out.println("ReedTrans." + (dcnt++) + ": " + s);
  } 
}

//// END ////

