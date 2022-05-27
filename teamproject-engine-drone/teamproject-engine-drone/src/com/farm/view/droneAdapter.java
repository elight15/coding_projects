package com.farm.view;

import java.io.IOException;
import main.java.surelyhuman.jdrone.control.physical.tello.*;
import java.lang.Math;


public class droneAdapter implements animationInterface{
	
	TelloDrone tdrone;
	
	int hold, speedy, Wturn, Hturn, slide, Xcm, Ycm, Zcm, goY, goX, gothere, homeAngle,  itemAngle = 0;
	
	/**
	 * Not sure how to get x,y coordinate for drone to fly to.
	 * @throws IOException 
	 * @throws InterruptedException 
	 */
	@Override
	public void visitItem(double x, double y, double z) throws IOException, InterruptedException {
		
		tdrone = new TelloDrone();
		hold = 5; speedy = 40; Hturn = 180; Wturn = 360; 
		
		/** 
		 * Get physical drones correct distance to travel.
		 * */
	     
	     Xcm = (int)((x/25.0)*30.0);
	     Ycm = (int)((y/25.0)*30.0);
	     Zcm = (int)((z/25.0)*30.0);
	     
	     /**
		     * Start SIMPLE physical drone flight program. 
		  **/
     System.out.println("Drone Visiting Item...");
     tdrone.activateSDK();
     tdrone.takeoff();
     tdrone.increaseAltitude(Zcm);
     tdrone.gotoXY(Xcm,-Ycm,speedy);
     tdrone.turnCCW(Wturn);
     tdrone.gotoXY(-Xcm, Ycm, speedy);
     System.out.println("Drone Return To Base..."); 
     tdrone.decreaseAltitude(Zcm);
     tdrone.land();
     tdrone.end();
	 
     /** 
      * Get degree of turn to item if using complex flight code.
      */
     itemAngle = (int) Math.toDegrees(Math.atan2(Ycm,Xcm));
     homeAngle = Hturn - itemAngle;
     
     /**
      * Get distance to travel if using complex flight code.
      */
     goY = Math.abs(Ycm - 0);
     goX = Math.abs(Xcm - 0);
     gothere = (int) Math.hypot(goY, goX);
     
	     /**
		     * Start COMPELX physical drone flight program. 
		  
        System.out.println("Drone Visiting Item...");
        tdrone.activateSDK();
        tdrone.takeoff();
        tdrone.increaseAltitude(Zcm);
        tdrone.turnCCW(itemAngle);
        tdrone.flyForward(gothere);
        tdrone.turnCW(Wturn);
        tdrone.turnCW(Hturn);
        tdrone.flyForward(gothere);
        tdrone.turnCCW(homeAngle);
        System.out.println("Drone Return To Base..."); 
        tdrone.decreaseAltitude(Zcm);
        tdrone.land();
        tdrone.end();
		**/
	}

	@Override
	public void scanFarm(double x, double y, double z) throws IOException, InterruptedException {
		tdrone = new TelloDrone();
		speedy = 80;
		
		/** 
		 * Get physical drones correct distance to travel.
		 * */
		 Xcm = (int)((x/25.0)*30.0);
	     Ycm = (int)((y/25.0)*30.0);
	     Zcm = (int)((z/25.0)*30.0);
	     slide = (int)(Xcm/11.0);
	     
	    /**
	     * Start physical drone flight program.
	     **/
         
	    System.out.println("Drone Scanning Farm...");
	    tdrone.activateSDK();
	    tdrone.setSpeed(speedy);
	    tdrone.takeoff();
	    tdrone.increaseAltitude(Zcm);
        tdrone.flyLeft( Xcm); //move to the top right corner
        tdrone.flyForward(Ycm); //move down to bottom right corner
        tdrone.flyRight(slide); //move right by equal divisible distance
        tdrone.flyBackward(Ycm); //move back to top
		tdrone.flyRight(slide);  //move right by equal divisible distance
		tdrone.flyForward(Ycm); //move back to bottom
		tdrone.flyRight(slide);  //move right by equal divisible distance
		tdrone.flyBackward(Ycm); //move back to top
		tdrone.flyRight(slide);  //move right by equal divisible distance
		tdrone.flyForward(Ycm); //move back to bottom
		tdrone.flyRight(slide);  //move right by equal divisible distance
		tdrone.flyBackward(Ycm); //move back to top
		tdrone.flyRight(slide);  //move right by equal divisible distance
		tdrone.flyForward(Ycm); //move back to bottom
		tdrone.flyRight(slide);  //move right by equal divisible distance
		tdrone.flyBackward(Ycm); //move back to top
		tdrone.flyRight(slide);  //move right by equal divisible distance
		tdrone.flyForward(Ycm); //move back to bottom
		tdrone.flyRight(slide);  //move right by equal divisible distance
		tdrone.flyBackward(Ycm); //move back to top
		tdrone.flyRight(slide);  //move right by equal divisible distance
		tdrone.flyForward(Ycm); //move back to bottom
		tdrone.flyRight(slide);  //move right by equal divisible distance
		tdrone.flyBackward(Ycm); //move back to top
		System.out.println("Drone Return To Base...");
        tdrone.land();
        tdrone.end();
		
	}
	
	
	
}