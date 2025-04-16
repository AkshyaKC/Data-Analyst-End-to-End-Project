# Data-Analyst-End-to-End-Project

This project covers the full journey of a data analyst—from collecting data by scraping the FIFA25 website, to analyzing it using Python and SQL, and finally creating an interactive dashboard in Power BI to visualize the results.

![Screenshot 2025-04-16 154410](https://github.com/user-attachments/assets/6e4d3998-25b5-4a11-83da-ebdcf1bba14f)

🗃️ Database Schema
In this project, data from the FIFA25 ratings page on ea.com is being scraped and stored in a MySQL database. The database consists of two main tables: player_profile and player_stats.

### 📊 `players_profile`

| Column Name | Data Type | Description |
| --- | --- | --- |
| player_name | VARCHAR | Name of the player |
| age | INT | Age of the player |
| league | VARCHAR | League the player currently plays in |
| preferred_foot | VARCHAR | Preferred foot (e.g., Left or Right) |
| height_cm | INT | Player's height in centimeters | 
| weight_kg | INT | Player's weight in kilograms |
| alt_position | VARCHAR | Alternate playing positions |

### 📊 `players_stats`
| Column Name | Data Type | Description |
| --- | --- | --- |
| rank | INT | Player's overall rank on the FIFA25 list |
| player_name | VARCHAR | Player's name (linked to player_profile) |
| image_url | TEXT | URL of the player's image |
| nationality | VARCHAR | Nationality of the player |
|  club | VARCHAR | Club the player is signed with |
|  position | VARCHAR | Main playing position |
|  ovr | INT | Overall rating |
|  pac | INT | Pace |
|  pac+- | INT | Change in Pace compared to the previous FIFA version |
|  sho | INT | Shooting |
|  sho+- | INT | Change in Shooting compared to the previous FIFA version |
|  pas | INT | Passing |
|  pas+- | INT | Change in Passing compared to the previous FIFA version |
|  dri | INT | Dribbling |
|  dri+- | INT | Change in Dribbling compared to the previous FIFA version |
|  def | INT | Defending |
|  def+- | INT | Change in Defending compared to the previous FIFA version |
|  phy | INT | Physicality |
|  phy+- | INT | Change in Physicality compared to the previous FIFA version |
