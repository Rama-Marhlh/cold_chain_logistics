# cold_chain_logistics

### Cold Chain Logistics - Project Overview

I am developing a comprehensive monitoring system for cold chain logistics, built using **Streamlit**, to ensure real-time visibility into the movement and storage of temperature-sensitive goods. The project tracks the journey from importers to warehouses and finally to supermarkets, focusing on key environmental factors such as temperature and humidity. The system is designed to maintain compliance with regulations and prevent spoilage by identifying critical events like loading, unloading, door openings, and more.

### Transportation (Truck Monitoring)

The project begins with monitoring goods inside trucks during transportation from the importer to various storage facilities. Each truck is equipped with 10 sensors to track internal temperature, external temperature, and humidity. This allows us to detect events such as:

- **Loading** and **unloading** of goods
- **Door openings**, which can cause sudden temperature changes
- Potential power outages or system faults

The data from all 10 sensors inside the truck is aggregated to calculate an average temperature, providing a holistic view of the truck’s environment. This helps identify how external conditions affect the internal environment, especially during events like door openings.

### Warehouse Monitoring

Once goods reach the warehouses, they are stored in rooms, each containing multiple sensors to monitor the environment. For example, if a warehouse has 4 rooms, and each room contains 10 sensors:

- The system monitors the temperature and humidity in each room.
- Data from the sensors in each room is aggregated to give the overall temperature for that room.
- The temperatures from all rooms are further aggregated to provide insights into the entire building’s behavior.

Additionally, tracking events such as **door openings**, **loading/unloading**, and **cleaning** allows us to evaluate their impact on temperature fluctuations.

### Supermarket Monitoring

After the goods leave the warehouse, they are delivered to supermarkets for retail. In this phase:

- Each supermarket has multiple rooms (e.g., 2 supermarkets with 2 rooms each), and each room is equipped with 8 sensors.
- The system monitors the internal and external temperature of each room, aggregating the sensor data to determine the room’s overall behavior.
- The aggregated data for both rooms in each supermarket provides a clear picture of temperature control at the store level.

### Customizable Monitoring

The system also allows for monitoring multiple trucks, warehouses, and supermarkets by selecting the respective company names. This way, instead of tracking specific rooms or trucks by number (as in earlier demos), users can monitor the logistics chain based on the company’s operational structure.

This idea was demonstrated in the recent Cold Chain Logistics demo, showcasing the ability to track and aggregate sensor-level data at various stages to ensure temperature compliance and event detection.
