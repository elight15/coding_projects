package com.farm.farmdashboard.items;

public class ItemVisitor implements Visitor{
	private double totalPrice, totalMarket;
	
	public ItemVisitor()
	{
		totalPrice = 0;
		totalMarket = 0;
	}

	@Override
	public void visit(Item item) {
		totalPrice += item.getPrice();
		totalMarket += item.getMarket();
	}

}
