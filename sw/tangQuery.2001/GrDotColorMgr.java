/// Color fader
/// By Brygg Ullmer, MIT Media Lab
/// Begun April 29, 2002
///

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.*;

import javax.swing.*;
import java.io.*;

///////////////////////////////////////////////////////////
////////////////////  GrDotColorMgr ///////////////////////
///////////////////////////////////////////////////////////

public class GrDotColorMgr {

//  Color mainColor  = new Color(212,187,18, 90);
//  Color mainColor  = new Color(242,207,18, 90);
  Color mainColor  = new Color(224,170,15, 90);

  Color arrivingColorTarget = new Color(212,32,18, 75);
  Color arrivingColors[];
  int   arrivingIncrements = 9;

  Color departingColorTarget = new Color(50,50,80,0);
  Color departingColors[];
  int   departingIncrements = 4;

  Hashtable id2arriving  = null;
  Hashtable id2departing = null;

  Hashtable idPresent  = null;
  Hashtable currentIds = null;
  Hashtable lastIds    = null;

  Boolean placeholder = new Boolean(true);

///////////////////////////////////////////////////////////
///////////////////////  METHODS //////////////////////////

///////////////////// getColor //////////////////////////

 public Color getColor(Integer key) {

  // if ID is not arriving or departing, it's the main color

   if (idPresent.containsKey(key) == true &&
       id2arriving.containsKey(key) == false &&
       id2departing.containsKey(key) == false) {

     // delete from "last"
     if (lastIds.containsKey(key)) {
       lastIds.remove(key);
     }

     return mainColor;
   }

  // if ID doesn't exist & it's not departing, add it

   if (idPresent.containsKey(key) == false && 
       id2departing.containsKey(key) == false) {

     idPresent.put(key, placeholder);
     id2arriving.put(key, new Integer(arrivingIncrements));

    // delete from "last"
     if (lastIds.containsKey(key)) {
       lastIds.remove(key);
     }

    // if we've also been flagged as departing, clear all records
     if (id2departing.containsKey(key)) {
       id2departing.remove(key);
     }

     return arrivingColorTarget;
   }

  // if ID is arriving, do the right thing

   if (id2arriving.containsKey(key) == true) {

     Integer aIdx = (Integer) id2arriving.get(key);

     int idx = arrivingIncrements - aIdx.intValue();
     Color result = arrivingColors[idx];

    //store decrement value;
     idx = aIdx.intValue() - 1;

     if (idx <= 0) {
       id2arriving.remove(key);
     } else {  
       id2arriving.put(key, new Integer(idx));
     }

    // if we've also been flagged as departing, clear all records
     if (id2departing.containsKey(key)) {
       id2departing.remove(key);
     }

    // delete from "last"
     if (lastIds.containsKey(key)) {
       lastIds.remove(key);
     }

     return result;
   }

  // if ID is departing, do the right thing

   if (id2departing.containsKey(key) == true) {

     Integer aIdx = (Integer) id2departing.get(key);

     int idx = departingIncrements - aIdx.intValue();
     Color result = departingColors[idx];

    //store decrement value;
     idx = aIdx.intValue() - 1;

     if (idx <= 0) {
       id2departing.remove(key);
     } else {  
       id2departing.put(key, new Integer(idx));
     }

     return result;
   }

   return null;
 }

///////////////////// additionsComplete //////////////////////
  //return vector of all the leftovers in lastIds
  //replace lastIds with a fresh copy

  public Vector additionsComplete() {

    Vector leftovers = new Vector();

   // get a list of the leftovers
    Enumeration leftoverKeys = lastIds.keys();

   // delete them from "present" list

    for (; leftoverKeys.hasMoreElements(); ) {

      Object key = leftoverKeys.nextElement();

      idPresent.remove(key);
      leftovers.addElement(key);

     // if listed as "arriving," remove
      if (id2arriving.containsKey(key)) {
        id2arriving.remove(key);
      }

      id2departing.put(key, new Integer(departingIncrements));
    }

   // add to leftovers those that are already departing

    Enumeration stragglerKeys = id2departing.keys();

    for (; stragglerKeys.hasMoreElements(); ) {

      Object key = stragglerKeys.nextElement();
      leftovers.addElement(key);
    }

   // replace lastIds with a fresh copy

    lastIds = (Hashtable) idPresent.clone();

   // freshen and return the leftovers

    return leftovers;
  }

///////////////////// GrDotColorMgr //////////////////////////

 public GrDotColorMgr() {

   /// setup color fades ///

   idPresent    = new Hashtable();
   id2arriving  = new Hashtable();
   id2departing = new Hashtable();

   currentIds     = new Hashtable();
   lastIds        = new Hashtable();

   int valMainColor[]      = colorToInts(mainColor);
   int valArrivingColor[]  = colorToInts(arrivingColorTarget);
   int valDepartingColor[] = colorToInts(departingColorTarget);

   // Allocate their arrays

   arrivingColors  = new Color[arrivingIncrements];
   departingColors = new Color[departingIncrements];

   // Calc the arriving colors

   int arrivingColorIncr[] = diffInts(valArrivingColor, valMainColor, 
                                      4, arrivingIncrements);

   int c[] = colorToInts(arrivingColorTarget);

   for (int i=0; i<arrivingIncrements; i++) {

     c = addInts(c, arrivingColorIncr, 4);
     arrivingColors[i] = new Color(c[0], c[1], c[2], c[3]);
   }

   // Calc the departing colors

   int departingColorIncr[] = diffInts(valMainColor, valDepartingColor, 
                                        4, departingIncrements);

   c = colorToInts(mainColor);

   for (int i=0; i<departingIncrements; i++) {

     c = addInts(c, departingColorIncr, 4);
     departingColors[i] = new Color(c[0], c[1], c[2], c[3]);
   }

 }

///////////////////// colorToInts //////////////////////////

 public int[] colorToInts(Color targColor) {

   if (targColor == null) {
     dbg("colorToInts passed a null!");
     return null;
   }

   int result[] = new int[4];

   result[0] = targColor.getRed();
   result[1] = targColor.getGreen();
   result[2] = targColor.getBlue();
   result[3] = targColor.getAlpha();

   return result;
 }

///////////////////// diffInts //////////////////////////

 public int[] diffInts(int a[], int b[], int size, int divisor) {

   int result[] = new int[size];

   for (int i=0; i<size; i++) {
     result[i] = (b[i] - a[i]) / divisor;
   }

   return result;
 }

///////////////////// addInts //////////////////////////

 public int[] addInts(int a[], int b[], int size) {

   int result[] = new int[size];

   for (int i=0; i<size; i++) {
     result[i] = a[i] + b[i];
   }

   return result;
 }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("GrDotColorMgr." + (dcnt++) + ": " + s);
  } 
} 

/// END ///

