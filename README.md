# Fiber-Competitve-Intensity-Model

## Background

Fiber Internet, also known as fiber-optic fixed broadband, is a high-speed internet connection that uses fiber-optic cables to transmit data. These cables are made up of thin strands of glass or plastic that use light to transmit data at incredibly fast speeds. Fiber internet has become increasingly popular over the years due to its speed, reliability, and overall efficiency.

With an increase in remote working, schooling, and socializing, there is a need for secured high-speed internet connectivity. Government bodies are increasing investments in fiber deployment, there is a rise in demand for fiber optics in the health sector for real-time patient monitoring, there is a rise in demand for data centers and 5G is expected to create new opportunities for the fiber optics network. With all these, the fiber-optics market is expected to reach $18 billion with a CAGR of 9.24% in 2028 according to Mordor Intelligence.

In this project, my team builds an ML algorithm that is capable of predicting the fiber internet uptake rate for a geographical polygon in South Africa. The team also developed a web interface visualizing the map of South Africa on the province, municipality, and ward level of granularity alongside their predicted fiber uptake rate. This web application can be queried to predict fiber uptake rate at any level of granularity given the right feature values.

This interactive web interface will enable Telco companies to quickly obtain the predicted fiber uptake rate for any polygon in South Africa and then apply the right formulas to compute the estimated revenue to be generated from that polygon, should fiber internet be rolled out in that area.

## Problem Statement

Fiber roll-out is done by the Telco companies but fiber cannot be rolled out randomly to any location. This is because fiber is not cheap and not everyone can afford fiber optics. Furthermore, the cost of installing fiber can have a significant impact on the pricing of fiber in that region. Telco companies need to make a return for every fiber that is rolled out and to achieve this, they need information about regions with good business prospects so as to roll out fiber in that region. Telco companies at the moment only have solutions that can provide information on the cost of rolling out fiber in a region. But, knowing the cost without knowledge of the estimated revenue nor ROI makes no business sense.

## Solution

Streamlit is the interactive web application tool that is used in this project for creating an interactive web application that is capable of visualizing the predicted fiber-optics uptake rate, and other key metrics up to the ward-level granularity in South Africa. Also, by integrating the best-performing model into Streamlit, the web application is capable of predicting fiber uptake rates at any level of granularity when provided with the feature values for prediction. These data-driven predictions will improve the accuracy of fiber roll-out to areas with good business prospects.
![streamlit_landing_page](https://github.com/olisa-clement/Fiber-Competitve-Intensity-Model/assets/77712936/6f9446cc-0dd8-47a6-bcf8-907bae1c6812)

## Methodology

The methodology employed in this project encompasses a comprehensive approach to achieving the project objectives. This includes data collection, pre-processing, uptake rate computation, model development, and web application development. These are easily summarized with the project flow diagram
![fiber_process_flow](https://github.com/olisa-clement/Fiber-Competitve-Intensity-Model/assets/77712936/4dc10153-7394-4b65-af6a-b7eb58e04e0e)

## Conclusion

The algorithm highlights average income, education, age distribution, and infrastructure as strong predictors of fiber uptake in South Africa. By integrating this model into the web application, we are able to predict the fiber uptake rate for any level of granularity given the values of the predictors. With this product, Telco companies can easily understand the predicted fiber uptake rate for any geographical region and use that information to make informed decisions on areas of fiber roll-out.
