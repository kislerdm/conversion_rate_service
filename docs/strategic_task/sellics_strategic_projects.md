# Sellics - Strategic Data Science Projects

The problem is stated in [here](../instructions/strategical_test-HoDS.pdf). I would formulate the objective of the task as how to maximize Sellics clients long-term *profit* by 

- employing machine learning for status quo Sellics ecosystem
- (potentially) introducing new machine learning driven services into the Sellics ecosystem.

## Problem Statement/Objective

The problem can be translated as a mathematical problem of optimization, where *profit* is the main *maximization objective*. 

First question to answer would be, how *profit* is defined? I would assume the following definitions:

```
profit = revenue - costs;

revenue = price * sales;

costs = suppy_costs + warehouse_costs + user_acquisition_costs + shipment_costs + return_costs;

price = f1(time, rating, product_market_value, product_meta, price ...) <- price is a function of time, rating (users satisfaction), product market value and demand, product meta data (qualities) and the price itself (price elasticity effect);

sales = f2(time, rating, product_market_value, price, product_meta, ...) <- sales is a function of time, rating, product market value and demand, price and product meta data (qualities);

suppy_costs = f3(time, product_market_value, product_meta, supplier_meta) <- the costs associated with the goods supply, how much an item of goods requires to invest. It's a function of time, goods market value, product qualitites and supplier qualities (distance, associated taxes etc.);

warehouse_costs = f4(time, product_meta) <- the costs associated with storage. It depends on time and product qualities (some goods may require special conditions for storage);

user_acquisition_costs = f5(time, product_meta, product_market_value, merchant_meta) <- the costs associated with marketing

shipment_costs = f6(time, product_meta, product_market_value, warehouse_meta, customer_meta) <- the costs associated with spendings on goods delivery to/from customers;

return_costs = f7(time, product_meta, product_market_value, rating, warehouse_costs, shipment_costs, suppy_costs) <- the costs associated with the spendings on warranty and goods return cases.

```

All profit related "ingredients" are cross-correlated time-series functions (**f1-f7**) of many parameters, which makes the formulated optimization problem being resolvable only by applying computational methods of data patterns extraction a.k.a. machine learning :)

### Problem Breakdown

On a high level, *the right balance between price and costs* for a goods unit to be defined. It can be broken down into the tasks:

- Maximize revenue:
  - Maximize sales at a given price
  - Set optimal price for highest possible sales

- Minimize costs:
  - Optimize supply costs
  - Find the best (price-/quality-wise) storage option
  - Reduce user_acquisition_costs
  - Reduction of spendings on user acquisition
  - Reduce goods return cases


## Status Quo Ecosystem

Based on the ecosystem [description](../instructions/strategical_test-HoDS.pdf), the Sellics services cover marketing (user acquisition), warehouse and pricing optimization/recommendation points for the profit optimization.

## Ideas for Potential Sellics Services

### Conversion Optimization

#### Goods Listing

One of existing services allow Sellics customers to edit their products listing which can positively influence shoppers conversion and reduce users acquisition costs. Many merchants (especially small ones) however may not have good quality images, or videos to describe their goods. Sellics may offer a service to improve image quality and increase users conversion. idealo.de had a similar idea, their implementation can be found [here](https://github.com/idealo/image-super-resolution).



### Supply Costs Optimization

- Build a recommender system for suppliers/manufactures where merchants can buy goods for retail at a lowest price and highest goods quality based on the data of suppliers current merchants may be willing to share (or do share already)
- Build a ranking system for fair product market value estimation to help clients negotiating supply costs with suppliers/manufactures
- Build a service for time-series forecast on when and how much of the goods to be bought to reduce the supply costs

### Return Probability Service

Build a service to predict probability of a goods unit to be returned back based on the goods meta data, its market value and demand, product rating and shopper satisfaction. The service would be aiming to reduce merchants costs associated with warranty/shipment/storage and recycling. The service would also serve as a proxy to shoppers satisfaction optimization/product rating improvement.

### Shipment Optimization Service

I may assume that fair amount of Sellics customers use amazon delivery system. I, as a recurring amazon buyer, was quite upset with their delivery service in Berlin, ergo I'd prefer to buy from a merchant using the shipment carrier other then the amazon one (this may be an issue for the German market though :) ).

On that basis, it seems a fair assumption that a service to optimize shipment *warehouse2shopper* would be quite beneficial to improve shoppers satisfaction and reduce spendings on marketing by increasing number of recurring shoppers. The service can provide a ranking/recommender system to pick a right delivery carrier from the costs, speed and real-time tracking point of view.

Another shipment optimization service, the *supplier2warehouse* shipment optimizer can be integrated under the Sellics services umbrella. The service can give be a recommender for merchants to pick a right carrier get the goods from supplier. The "definition of right" may be formulated as, to deliver goods from supplier/manufacturer at right time (defined by demand) at lowest price. This service should help to reduce shipment costs (and to set fair costs) and to simplify the supply-demand balance forecast.