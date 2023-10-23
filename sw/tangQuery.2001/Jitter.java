// Jitter module
// By Brygg Ullmer, MIT Media Lab
// Begun April 25, 2002

//////////////////////////////////////////////////////////////
///////////////////////////// jitter /////////////////////////
//////////////////////////////////////////////////////////////

public class Jitter {

  int jitterRange;
  int jitterMax;

  int jitterArray[];

////////////////////  addJitter /////////////////////////////
  
  public Jitter(int jitterRange, int jitterMax) {

    this.jitterRange = jitterRange;
    this.jitterMax   = jitterMax;

    jitterArray = new int[jitterMax];

    for (int i=0; i<jitterMax; i++) {
      jitterArray[i] = -1;
    }
  }


////////////////////  addJitter /////////////////////////////

  public int addJitter(int indexVal) {

    int modIndexVal = indexVal % jitterMax;
    
   // if the val exists, use it

    if (jitterArray[modIndexVal] != -1) {
      return jitterArray[modIndexVal];
    }

   // if not, generate it

    int jitter = (int) (Math.random() * jitterRange); 
    jitterArray[modIndexVal] = jitter;

    return jitter;
  }
}

/// END ///

