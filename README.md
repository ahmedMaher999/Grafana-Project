
# 📊 Grafana Project – IRS Data Dashboard

This project visualizes simulated IRS tax data using Flask, MySQL, Docker, and Grafana. It seeds fake taxpayer and tax return data, then exposes it for live visualization through Grafana dashboards.

---

## 🚀 How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/grafana-project.git
cd grafana-project
```

### Step 2: Build and start the services

```bash
docker-compose up --build
```

This command will:
- Build the Flask app container
- Start a MySQL database
- Expose the Flask API on port `5000`

### Step 3: Seed the database

Open your browser and go to:

```
http://localhost:5000/seed-database
```

This will return that Database seeded successfully!.

---

## 📊 Connect Grafana to MySQL

> ⚠️ Ensure you have Grafana installed and running locally on port `3000`.

### Steps to add the data source:

1. Open Grafana at [http://localhost:3000](http://localhost:3000)
2. Login using default credentials (`admin` / `admin`)
3. Go to **Configuration → Data Sources → Add data source**
4. Select **MySQL**
5. Enter the following details:
   - **Host**: `localhost:3306`
   - **Database**: `irs_data`
   - **User**: `irs_user`
   - **Password**: `password123`
6. Click **Save & Test**

You should see a green success message indicating the connection is working.

---

## 🧾 Dashboard Queries & Visualizations

### 1️⃣ Total Tax Paid by Year (XY Chart)

**SQL Query:**
```sql
SELECT year, SUM(tax_paid) AS total_tax_paid
FROM returns
GROUP BY year
ORDER BY year;
```

- **Visualization Type**: Time Series Line Chart
- **X-Axis**: Year
- **Y-Axis**: Total Tax Paid

---

### 2️⃣ Refunds by State (Table)

**SQL Query:**
```sql
SELECT state, SUM(refund) AS total_refunds
FROM taxpayers t
JOIN returns r ON t.id = r.taxpayer_id
GROUP BY state;
```

- **Visualization Type**: Table
- **Columns**: State, Total Refunds
- Helps identify which states received the highest refunds.

---

### 3️⃣ Number of Filings per Year (Trend Chart)

**SQL Query:**
```sql
SELECT year, COUNT(*) AS filings
FROM returns
GROUP BY year;
```

- **Visualization Type**: Bar or Line Chart
- **X-Axis**: Year
- **Y-Axis**: Number of Tax Filings
- Tracks how many filings were submitted per year.

---

## 🖼 Dashboard Example

Below is a sample of the Grafana dashboard created using the above queries:

![Grafana Dashboard](images/dashboard.png)

---

## 🧰 Tech Stack

- **Flask** (API & seeding)
- **MySQL** (Database)
- **Faker** (Mock data)
- **Docker + Compose** (Containerization)
- **Grafana** (Visualization)

---

## 🐳 Docker Overview

### `docker-compose.yml`

```yaml
services:
  flask-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      MYSQL_HOST: mysql-db
      MYSQL_USER: irs_user
      MYSQL_PASSWORD: password123
      MYSQL_DATABASE: irs_data
    depends_on:
      - mysql-db

  mysql-db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: irs_data
      MYSQL_USER: irs_user
      MYSQL_PASSWORD: password123
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

---

## 📎 Notes

- To access the MySQL shell:
```bash
docker exec -it mysql-db mysql -u irs_user -p
# Password: password123
```

- To test API:
```bash
curl http://localhost:5000/total-revenue
```

---

## 📬 Author

Made with ❤️ by [Your Name]  
This is part of a DevOps data visualization project using Grafana and Docker.


