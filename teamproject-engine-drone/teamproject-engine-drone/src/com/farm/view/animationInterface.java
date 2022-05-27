package com.farm.view;

import java.io.IOException;

public interface animationInterface {
	// visit item and scan farm from animation
	public void visitItem(double x, double y, double z )throws IOException, InterruptedException;
	public void scanFarm(double x, double y,double z) throws IOException, InterruptedException;
}
