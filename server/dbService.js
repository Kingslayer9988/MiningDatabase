const mysql = require('mysql');
const dotenv = require('dotenv');
const fs = require('fs');
let instance = null;
dotenv.config();

const connection = mysql.createConnection({
    host: process.env.HOST,
    user: process.env.USERNAME,
    password: process.env.PASSWORD,
    database: process.env.DATABASE,
    port: process.env.DB_PORT,
    // Dunno how SSL WORKS! :(
    ssl: {
        key: fs.readFileSync('ca-key.pem'),
        cert: fs.readFileSync('ca-cert.pem'),
        rejectUnauthorized: false,
      }
});

connection.connect((err) => {
    if (err) {
        console.log(err.message);
    }
    // console.log('db ' + connection.state);
});


class DbService {
    static getDbServiceInstance() {
        return instance ? instance : new DbService();
    }

    async getAllData() {
        try {
            
            const response = await new Promise((resolve, reject) => {
                const query = "SELECT * FROM xmrig ORDER BY id DESC LIMIT 20;";

                connection.query(query, (err, results) => {
                    if (err) reject(new Error(err.message));
                    resolve(results);
                })
            });
        
            // console.log(response);
            return response;
        } catch (error) {
            console.log(error);
        }
    }
    async searchByName(name) {
        try {
            const response = await new Promise((resolve, reject) => {
                const query = "SELECT * FROM xmrig WHERE user = ? ORDER BY id DESC LIMIT 20;";

                connection.query(query, [name], (err, results) => {
                    if (err) reject(new Error(err.message));
                    resolve(results);
                })
            });

            return response;
        } catch (error) {
            console.log(error);
        }
    }
}

module.exports = DbService;