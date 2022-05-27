package com.farm.farmdashboard.items;

import java.util.ArrayList;

public interface Item {
    // Setters
    public void setName(String name);
    public void setPrice(double price);
    public void setPosition(int x, int y);
    public void setDimensions(int length, int width, int height);
    public void setMarket(double marketVal);

    // Getters
    public String getName();
    public double getPrice();
    public int getPosX();
    public int getPosY();
    public int getLength();
    public int getWidth();
    public int getHeight();
    public double getMarket();

    // Children
    public ArrayList<Item> getChildren();
    public void addChild(Item item);
    public void removeChild(Item item);

    // Iteration
    public Item next();
    public boolean hasNext();
    
    // Visitor
    public abstract void accept(Visitor vis);
}
