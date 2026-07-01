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

        <div className="auth-screen">

            <form className="auth-card" onSubmit={login}>

                <div className="auth-mark">TM</div>

                <h2>Welcome back</h2>

                <p className="auth-sub">Log in to pick up where you left off.</p>

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

                <button className="btn btn-primary">

                    Login

                </button>

                {error &&

                    <p className="auth-error">{error}</p>

                }

                <p className="auth-footer">

                    New here? <Link to="/register">Create an account</Link>

                </p>

            </form>

        </div>

    );

}
