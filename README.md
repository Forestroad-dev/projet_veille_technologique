## Run Locally

1. Clone repo

   ```shell
    $ git clone https://github.com/Forestroad-dev/projet_veille_technologique.git
    $ cd next-amazona-v2
   ```

2. Setup MongoDB

   - Local MongoDB
     - Install it from [here](https://www.mongodb.com/try/download/community)

     - Create database 
     - In .env file update MONGODB_URI=mongodb+srv://your-db-connection

3. Install and Run

   ```shell
     npm install
     npm run dev
   ```

4. Seed Data

   - Run this on browser: http://localhost:3000/api/products/seed
   - It returns admin email and password and 6 sample products

5. Admin Login

   - Run http://localhost:3000/signin
   - Enter admin email "admin@gmail.com" and password "admin" and click Signin
