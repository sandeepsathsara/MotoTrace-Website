const express = require("express");
const cors = require("cors");
const pool = require("./db");
const bcrypt = require("bcrypt");

const app = express();
app.use(cors());
app.use(express.json());

// Register
app.post("/register", async (req, res) => {
  const { name, email, password } = req.body;
  try {
    const hashed = await bcrypt.hash(password, 10);
    await pool.query(
      "INSERT INTO users (name, email, password) VALUES ($1, $2, $3)",
      [name, email, hashed]
    );
    res.status(200).json({ message: "User registered" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Registration failed" });
  }
});

// Login
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  try {
    const result = await pool.query("SELECT * FROM users WHERE email=$1", [email]);
    const user = result.rows[0];
    if (user && await bcrypt.compare(password, user.password)) {
      res.json({ message: "Login successful" });
    } else {
      res.status(400).json({ message: "Invalid credentials" });
    }
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Login error" });
  }
});

app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
