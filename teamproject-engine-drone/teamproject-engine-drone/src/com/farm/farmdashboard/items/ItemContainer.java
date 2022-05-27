package com.farm.farmdashboard.items;

import java.util.ArrayList;

public class ItemContainer extends ItemLeaf {
    ArrayList<Item> children;
    private int index = 0;

    public ItemContainer(String name, double price, int x, int y, int l, int w, int h, ArrayList<Item> children) {
        this.name = name;
        this.price = price;
        posX = x;
        posY = y;
        length = l;
        width = w;
        height = h;
        this.children = children;
    }

    public void addChild(Item item) {
        children.add(item);
    };
    
    public void removeChild(Item item) {
    	children.remove(item);
    }

    public ArrayList<Item> getChildren() {
        return children;
    }

    public boolean hasNext() {
        if (index == children.size()) {
            index = 0;
            return false;
        }
        return index < children.size();
    }

    public Item next() {
        Item nextItem = this.children.get(index);
        index++;
        return nextItem;
    }
    
    public double getPrice() {
    	double priceTot = 0;
    	while (this.hasNext()) 
    	{
    		Item currentItem = (Item)this.next();
    		priceTot += currentItem.getPrice();
    	}
    	return this.price + priceTot;
    }
    
    public double getMarket() {
    	double marketTot = 0;
    	while (this.hasNext()) 
    	{
    		Item currentItem = (Item)this.next();
    		marketTot += currentItem.getMarket();
    	}
    	return marketTot;
    }
}
