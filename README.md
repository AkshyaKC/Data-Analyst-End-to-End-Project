# Data-Analyst-End-to-End-Project

This project covers the full journey of a data analyst—from collecting data by scraping the FIFA25 website, to analyzing it using Python and SQL, and finally creating an interactive dashboard in Power BI to visualize the results.

![Screenshot 2025-04-16 154410](https://github.com/user-attachments/assets/6e4d3998-25b5-4a11-83da-ebdcf1bba14f)

🗃️ Database Schema
In this project, data from the FIFA25 ratings page on ea.com is being scraped and stored in a MySQL database. The database consists of two main tables: player_profile and player_stats.

🔹 player_profile
Column Name | Data Type | Description
player_name | VARCHAR | Name of the player
age | INT | Age of the player
league | VARCHAR | League the player currently plays in
preferred_foot | VARCHAR | Preferred foot (e.g., Left or Right)
height_cm | FLOAT | Player's height in centimeters
weight_kg | FLOAT | Player's weight in kilograms
alt_position | JSON | Alternate playing positions (stored as JSON array)
