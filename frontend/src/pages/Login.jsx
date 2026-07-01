import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import api from "../services/api";

export default function Login() {

    const navigate = useNavigate();

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const [error, setError] = useState("");

    async function login(e) {

        e.preventDefault();

        try {

            const res = await api.post("/auth/login", {

                email,

                password

            });

            localStorage.setItem("token", res.data.token);

            localStorage.setItem("role", res.data.role);

            navigate("/dashboard");

            window.location.reload();

        }

        catch (err) {

            setError(

                err.response?.data?.message ||

                "Login failed."

            );

        }

    }

    return (

        <div className="container">

            <form className="card" onSubmit={login}>

                <h2>Login</h2>

                <input
                    placeholder="Email"
                    value={email}
                    onChange={(e)=>setEmail(e.target.value)}
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e)=>setPassword(e.target.value)}
                />

                <button>

                    Login

                </button>

                {error &&

                    <p>{error}</p>

                }

                <Link to="/register">

                    Create Account

                </Link>

            </form>

        </div>

    );

}