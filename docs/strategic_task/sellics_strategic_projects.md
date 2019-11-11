# Sellics - Strategic Data Science Projects

**By Dmitry Kisler - www.dkisler.com**

The problem is stated in [here](../instructions/strategical_test-HoDS.pdf). I would formulate the objective of the task as how to maximize Sellics clients long-term *profit* by 

- employing machine learning for status quo Sellics ecosystem
- (potentially) introducing new machine learning driven services into the Sellics ecosystem.

## Problem Statement/Objective

The problem can be translated as a mathematical problem of optimization, where *profit* is the main *maximization objective*. First question to answer would be, how *profit* is defined? I would assume the following definitions:

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

Based on the ecosystem [description](../instructions/strategical_test-HoDS.pdf), the Sellics services cover marketing (user acquisition), warehouse and pricing optimization/recommendation points for the profit optimization. I may propose the following features/services which can be integrated under the Sellics services umbrella to benefit its customers and hence can benefit Sellics.

## Ideas for Potential Sellics Services

### Conversion Optimization

#### Marketing Optimization

A service automatic bidding on keywords based on ROI could be built and offered to Sellics customers. The service shall consider goods price, quality, its market value and demand, merchant and item rating, PPC and CTR and "compare" that to number of acquired users and revenue they brought to merchant. For example, the service can track ROI of a keywords/marketing campaign in terms of its ranking for amazon and in terms of its impact on the merchant revenue and recommend (apply recommendation automatically) to either stop bidding on a given keyword, or to scale the bidding to acquire even more users.

#### Goods Listing

One of existing services allow Sellics customers to edit their products listing which can positively influence shoppers conversion and reduce users acquisition costs. Many merchants (especially small ones) however may not have good quality images, or videos to describe their listing items. Sellics could offer a service to improve image quality and increase users conversion. idealo.de had a similar idea, their implementation can be found [here](https://github.com/idealo/image-super-resolution).

</br>

#### Description Curation

Text description of the goods may be quite impactful on the users conversion, hence a service to curate (NLP problem) merchant provided items description could be offered by Sellics. The service can provide recommendation for description words replacement, description shortening and key facts extraction from text. Listed service features aim to improve users/shoppers experience and would increase organic conversion and potentially increase number of recurring shoppers.  

#### Keywords Recommendation

Proper set of keywords describing the product is the foremost ingredient of user acquisition success. A service to recommend keywords to be associated with a merchant's product could be offered to maximize shoppers conversion. Recommendation to be based on the product description (NLP, or image recognition task), keywords ranking, product quality and meta data, market value and price.

### Pricing Recommender System

Sellics customers may have an access to competitors pricing to improve their products ranking through shoppers conversion. A price recommender service could be offered as extension to existing pricing service. The recommender/optimizer may suggest to discount/rise price for specific products at specific time of the day depending on the market/demand situation, merchant inventory, merchant and product rating. As a followup/second step, the recommender service can offer automated price adjustment (rule-based -> time-series forecast with LSTM/RNN -> reinforcement learning/multi-arm bandit problem).

### Revenue, Supply-demand Forecast

Many SME  face the problem of underestimating demand, or overestimating supply and run out of cash they could reinvest within less then a year from the date of foundation. Sellics could help small/intermediate merchants by providing a service to forecast and recommend amount of goods to be ordered from right supplier at right time, to forecast merchants revenue for upcoming quartile/6 months based on the inventory and market data so the merchant would be able to potentially fundraise and reconsider business strategy.

### Review Ranking/Summary

- To help merchants with business strategy and pricing, a service to give summary on reviews (NLP tasks) shoppers leave on the product can be provided by Sellics.
- Reviews auto-reply service could also be proposed. Review with merchant reaction are being perceived by shoppers better compares to the ones with no reaction.

### Supply Costs Optimization

- Build a recommender system for suppliers/manufactures where merchants can buy goods for retail at a lowest price and highest goods quality based on the data of suppliers current merchants may be willing to share (or do share already).
- Build a ranking system for fair product market value estimation to help clients negotiating supply costs with suppliers/manufactures.
- Build a service for time-series forecast on when and how much of the goods to be bought to reduce the supply costs.

### Return Probability Service

Build a service to predict probability of a goods unit to be returned back based on the goods meta data, its market value and demand, product rating and shopper satisfaction. The service would be aiming to reduce merchants costs associated with warranty/shipment/storage and recycling. The service would also serve as a proxy to shoppers satisfaction optimization/product rating improvement.

### Shipment Optimization Service

I may assume that fair amount of Sellics customers use amazon delivery system. I, as a recurring amazon buyer, was quite upset with their delivery service in Berlin, ergo I'd prefer to buy from a merchant using the shipment carrier other then the amazon one (this may be an issue for the German market though :) ).

On that basis, it seems a fair assumption that a service to optimize shipment *warehouse2shopper* would be quite beneficial to improve shoppers satisfaction and reduce spendings on marketing by increasing number of recurring shoppers. The service can provide a ranking/recommender system to pick a right delivery carrier from the costs, speed and real-time tracking point of view.

Another shipment optimization service, the *supplier2warehouse* shipment optimizer can recommend merchants to pick a right carrier get the goods from supplier. The "definition of right" may be formulated as, to deliver goods from supplier/manufacturer at right time (defined by demand) at lowest price. This service should help to reduce shipment costs (and to set fair costs) and to simplify the supply-demand balance forecast.

## Summary

The services suggested above can be considered to further Sellics towards becoming the industry standard tool if you want to (re-)enter amazon e-commerce market, or if you want to improve your positions there. The machine learning driven Sellics services should help merchants to cover every aspect from what supplier to pick and where to store goods to how to buy users with highest ROI, how to increase number of recurring shoppers and to reduce return cases.