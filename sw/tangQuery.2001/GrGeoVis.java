/// Plot test
/// By Brygg Ullmer, MIT Media Lab
/// Begun November 1, 2001
///
/// Based on threading template by Ben Fry (fry@media.mit.edu),
/// 4/18/2001, and WinHelp Java Tutorial: AnimatorApplication.java,
/// Arthur van Hoff

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.*;

import javax.swing.*;
import java.io.*;

///////////////////////////////////////////////////////////
////////////////////  GrGeoVis ////////////////////////////
///////////////////////////////////////////////////////////

public class GrGeoVis {

/////////////  METHODS ///////////////

// static void main(String args[])
// public GrGeoVis()
// public run()

/////////////  MEMBERS ///////////////

  float minLat = (float)  34.9195, maxLat = (float)  35.5366; //sp: .617
  float minLon = (float) -81.1907, maxLon = (float) -80.4977; //sp: .693

  float latRange = maxLat - minLat;
  float lonRange = maxLon - minLon;

  Font queryFont = new Font("Verdana", Font.PLAIN, 10);

  Font specialCoordFont = new Font("Verdana", Font.PLAIN, 16);

  Image bgImage;

  GrGlyphGen glyphMgr = null;

  GrDotColorMgr dotColorMgr = new GrDotColorMgr();

  GrRange grRange  = null;
  GrRange grRange2 = null;
  GrRange grRange3 = null;

  QRackMgr     qrackMgr = null; 
  QRackVis    parentVis = null; 
  BldgDbMgr   dbMgr = null;

//  String lastQuery = "", currentQuery = "";

  boolean dotOnly = true;
  //Color dotColor  = new Color(254,221,0, 80);

  Color dotColor  = new Color(212,187,18, 80);

  Color arrivingColorTarget = new Color(212,32,18, 60);
  Color arrivingColors[];
  int   arrivingIncrements = 5;

  Color departingColorTarget = new Color(64,100,181,50);
  Color departingColors[];
  int   departingIncrements = 3;

  Color queryStrBg = new Color(80,80,80,70);
  Color queryStrFg = new Color(75,75,75);

  int dotRadius = 4, dotDiam = 8;
  boolean resultsShown = false;

// Special coords live in BldgDbMgr

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  GrGeoVis /////////////////////////////

  public GrGeoVis(QRackMgr mgr, QRackVis parentVis) {

    this.parentVis = parentVis; 

    qrackMgr = mgr;
    dbMgr    = (BldgDbMgr) qrackMgr.getInterp().getDbMgr(); 
    glyphMgr = new GrGlyphGen();

    dbg("loading image");

  bgImage = 
   Toolkit.getDefaultToolkit().getImage("maps/charlotte-mapblast-380i.gif");

    if (bgImage == null) {
      dbg("can't find image");
    }

//    PTokModel ptok = qrackMgr.qrackModel.ptoksActive.getPTok("price");
//    if (ptok == null) {dbg("GrGeoVis const weirdness: price null");}

    grRange = new GrRange();
    grRange.setPixBounds(825, 1000, 900);
    grRange.bgPadY2 = 28;
    grRange.setFontSize(20);

    grRange.label = "price";
//    grRange.labelTagColor = ptok.paramColor;
//    grRange.labelTagColor = Color.red;
    grRange.labelTagColor = new Color(195, 85,85);

//    ptok = qrackMgr.qrackModel.ptoksActive.getPTok("acreage");
//    if (ptok == null) {dbg("GrGeoVis const weirdness: acreage null");}

    grRange2 = new GrRange();
    grRange2.setPixBounds(825, 1000, 840);
    grRange2.bgPadY2 = 28;
    grRange2.setFontSize(20);

    grRange2.label = "acreage";
//    grRange2.labelTagColor = new Color(50, 20, 150);
    grRange2.labelTagColor = new Color(35, 35, 235);
//    grRange2.labelTagColor = ptok.paramColor;
//    grRange2.labelTagColor = Color.blue;


    grRange3 = new GrRange();
    grRange3.setPixBounds(825, 1000, 780);
    grRange3.bgPadY2 = 28;
    grRange3.setFontSize(20);

    grRange3.label = "sqfoot";
//    grRange3.labelTagColor = new Color(50, 20, 150);
    grRange3.labelTagColor = new Color(100, 120, 250);
  }

////////////////////  scale coord /////////////////////////////

  public int[] scaleCoord(float lat, float lon) {

    float relX = (lat - minLat) / latRange;
    float relY = (lon - minLon) / lonRange;

    int result[] = new int[2];

    result[0] = (int)(relX * (float) parentVis.panelWidth);
    result[1] = (int)(relY * (float) parentVis.panelHeight);

   // nudge for registration:

    result[0] -= 40;
    result[1] -= 8;

    return result;
  }

////////////////////  id2coord /////////////////////////////

  Hashtable id2coord = new Hashtable();

  public int[] mapId2coord(Integer key) {

    if (id2coord.containsKey(key)) {

      int result[] = (int []) id2coord.get(key);
      return result;
    }

  // ok; generate & store it
    
    BldgRecord br     = dbMgr.getBldgId(key);
    if (br == null) {return null;}

    int coord[]       = scaleCoord(br.lat, br.lon);

    id2coord.put(key, coord);

    return coord;
  }

////////////////////  ptokEnters /////////////////////////////

  public void ptokEnters(PTokModel ptok) {

    int   tokId    = ptok.tokId;
    Color tokColor = ptok.paramColor;

    glyphMgr.setTokColor(tokId, tokColor);

dbg("ptokEnters; color set");
  }

////////////////////  ptokChanges /////////////////////////////

  public void ptokChanges(PTokModel ptok) {

    if (ptok.visLabel.compareTo("price") == 0) {
      if (ptok.getScaledUpper() > ptok.getUpperThresh()) {
        grRange.setBounds(ptok.getRatioLower(), 1);
      } else {
        grRange.setBounds(ptok.getRatioLower(), ptok.getRatioUpper());
      }
    } 

    if (ptok.visLabel.compareTo("acreage") == 0) {
      if (ptok.getScaledUpper() > ptok.getUpperThresh()) {
        grRange2.setBounds(ptok.getRatioLower(), 1);
      } else {
        grRange2.setBounds(ptok.getRatioLower(), ptok.getRatioUpper());
      }
    } 

    if (ptok.visLabel.compareTo("sqft") == 0) {
      if (ptok.getScaledUpper() > ptok.getUpperThresh()) {
        grRange3.setBounds(ptok.getRatioLower(), 1);
      } else {
        grRange3.setBounds(ptok.getRatioLower(), ptok.getRatioUpper());
      }
    } 
  }

////////////////////  plotCoords /////////////////////////////

  public void plotCoords(BufferedImage buffImg) {

   // Check to make things are OK to start

    if (dbMgr.recsLoaded == false) {
      dbg("plotCoords problem: data not yet loaded!");
      return;
    }

    Graphics2D h = buffImg.createGraphics();

     // Draw the "special locations"

      AffineTransform baseTransform = h.getTransform();
      h.setColor(Color.blue);
      h.setFont(specialCoordFont);

      if (dbMgr.specialCoordsExist) {
        for (int i=0; i<dbMgr.numSpecialCoords; i++) {
	  if (dbMgr.specialCoordPlot[i] == false) {continue;}

	 // OK -- do the right things.

	  double dpos[] = dbMgr.specialCoordPos[i];
	  int pos[] = scaleCoord((float) dpos[0], (float) dpos[1]);

//	  dbg("FOO: X " + pos[0] + " / Y " + pos[1]);

	  h.translate(pos[0], pos[1]);
	  h.rotate(Math.PI);

	  String drawStr = dbMgr.specialCoordName[i];

	  h.drawString(drawStr, 0, 0);
	  h.setTransform(baseTransform);
	}
      }

/*
    if (dbMgr.visQueryCompleted == false) {
      dbg("vis query not complete");
      return;
    }
*/

    Vector vect = qrackMgr.getModel().ptoksActive.getActivePToks();

    //int numToksActive = qrackMgr.qrackModel.getNumToksActive();
    int numToksActive = vect.size();

  /// Build representation of the active toks

    if (numToksActive == 0) {
      resultsShown = false;
      return;
    }
    resultsShown = true;

    PTokModel   ptoks[]  = new PTokModel[numToksActive];
    PTokResults ptokrs[] = new PTokResults[numToksActive];
    int         ptokid[] = new int[numToksActive];

    for (int i=0; i<numToksActive; i++) {
      ptoks[i] = (PTokModel) vect.elementAt(i);

      if (ptoks[i] == null) {
        dbg("plotCoords bogosity: null ptok!");
	return;
      }

      ptokid[i] = ptoks[i].tokId;

      ptokrs[i] = qrackMgr.getInterp().mapPTok2Results(ptoks[i]);

      if (ptokrs[i] == null) {
        dbg("plotCoords bogosity: null ptok result!");
	return;
      }
    }

   /// Render it to the screen

    int toksPresent[] = new int[numToksActive];

    try {

//      Enumeration ptokResultsEnum = 
//       qrackMgr.qrackInterp.getPTokResults();

      Enumeration visQueryEnum = dbMgr.getVisQueryResults();

      if (visQueryEnum == null) {
        dbg("plotCoords: visQueryEnum is null!");
	return;
      }

// draw points

      for (; visQueryEnum.hasMoreElements(); ) {

        Integer selBldgId = (Integer) visQueryEnum.nextElement();

        BldgRecord br     = dbMgr.getBldgId(selBldgId);
	if (br == null) {continue;}

	// OK; see who's participating

	int participatingToks = 0;

	try {
  	  for (int i=0; i<numToksActive; i++) {

//	    if (ptokrs[i].containsKey(br.bldg_id)) {
	      toksPresent[participatingToks] = ptokid[i];
	      participatingToks++;
//	    }
	  }
	} catch (Exception e) { 
	   dbg("plotCoords: inner loop exception: " + e.getMessage());
	   return;
	}
/*
	int glyph[] = glyphMgr.getGlyphPat(numToksActive,
	                     participatingToks, toksPresent);

        if (glyph == null) {
	  dbg("plotCoords: bogus glyph returned");
	  return;
	}
*/
	int coord[] = mapId2coord(selBldgId);

        //int coord[]       = scaleCoord(br.lat, br.lon);

        if (dotOnly) {
          Color dotColor = dotColorMgr.getColor(selBldgId); 

	  h.setColor(dotColor);

          h.fillRect(coord[0] - dotRadius, coord[1] - dotRadius, 
	             dotDiam, dotDiam);
        } else {   
//          plotPattern(coord[0], coord[1], glyph, buffImg);
	}
      }

     // Fade out those that are so inclined

      Vector fadingAway = dotColorMgr.additionsComplete();

      int size = fadingAway.size();

      for (int i=0; i < size; i++) {
	Integer key = (Integer) fadingAway.elementAt(i);
	int coord[] = mapId2coord(key);

	Color dotColor = dotColorMgr.getColor(key);
        h.setColor(dotColor);

        h.fillRect(coord[0] - dotRadius, coord[1] - dotRadius, 
	             dotDiam, dotDiam);
      }

    } catch (Exception e) {dbg("plotCoords exception: " + e.toString());}
  }

////////////////////  plotPattern /////////////////////////////

/*
  public void plotPattern(int x, int y, int pat[], BufferedImage buffImg) {

    //buffImg.setRGB(x, y, 3, 3, pat, 0, 3);
    //buffImg.setRGB(x, y, 9, 9, pat, 0, 9);
    //buffImg.setRGB(x, y, 9, 9, pat, 0, 9);

    try {
//      int x2 = parentVis.panelWidth  - x ;
//      int y2 = parentVis.panelHeight - y ;
// UNDOING, 04/27/02; we were flipped!

      buffImg.setRGB(x, y, 11, 11, pat, 0, 11);

      //buffImg.setRGB(x, y, 23, 23, pat, 0, 23);
    } catch (Exception e) {return;}
  }
*/
////////////////////  draw label /////////////////////////////

  public void drawLabel(Graphics h, int x, int y, Color labelColor,
                        String paramName, String lower, String upper) {

    int height = 75;
    int width  = 200;

    int padX = 10;
    int padY = 10;

    int colorTagSize = 20;

    Color bgColor   = new Color(75, 75, 75);
    Color textColor = Color.white;

    h.setColor(bgColor);
    h.fillRect(x, y, height, width);

    h.setColor(labelColor);
    h.fillRect(x + padX, y - padY, colorTagSize, colorTagSize);
  }

////////////////////  display Query /////////////////////////////

  public void displayQuery(Graphics2D h, String queryStr) {

    if (queryStr == null) {return;}

    int idx = queryStr.indexOf(" where ");

    if (idx == -1) {return;}  // don't display

    idx += 7;

    int end = queryStr.length() - 1;

    String displayStr = queryStr.substring(idx, end);

    AffineTransform baseTransform = h.getTransform();

    h.setColor(queryStrBg);
    h.fillRect(0, 7, parentVis.panelWidth, 15);

    h.setFont(queryFont);
    h.setColor(queryStrFg);

    int x1 = parentVis.panelWidth - 20;
    int y1 = 10;

    h.translate(x1,y1);
    h.rotate(Math.PI);

    h.drawString(displayStr, 0, 0);

    h.setTransform(baseTransform);
  }

////////////////////  paint /////////////////////////////

  public void paint(Graphics g) {

//if (dbMgr.visQueryCompleted == false) {return;}
//if (true) return;
  
  // Create compositing/alpha context

    BufferedImage buffImg = new BufferedImage(
      parentVis.panelWidth, parentVis.panelHeight, 
      BufferedImage.TYPE_INT_ARGB);

    //Raster data = bgImage.getData();

    Graphics2D gbi = buffImg.createGraphics();

    if (bgImage != null) {
      gbi.drawImage(bgImage, 0, 0, 
        parentVis.panelWidth, parentVis.panelHeight, null);

    } else {
      dbg("bgImage is null");
    }

    if (dbMgr.visQueryResultsExist == true) {
      plotCoords(buffImg);
    }

    Graphics2D h = (Graphics2D) g;

/*
    if (qrackMgr.getModel().ptoksActive.isPTokPresent("price")) {
      grRange.drawRange(gbi);
    }

    if (qrackMgr.getModel().ptoksActive.isPTokPresent("acreage")) {
      grRange2.drawRange(gbi);
    }

    if (qrackMgr.getModel().ptoksActive.isPTokPresent("sqft")) {
      grRange3.drawRange(gbi);
    }
*/
    if (dbMgr != null && dbMgr.lastQuery != null && resultsShown) {

      displayQuery(gbi, dbMgr.lastQuery);
    }

    h.drawImage(buffImg, null, 0, 0);

  // Draw framerate

    //g.drawString((int)updateRate + " fps", 5, 450);
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("GrGeoVis." + (dcnt++) + ": " + s);
  } 
}

//// END ////

