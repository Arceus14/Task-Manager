import { useState } from "react";

import { Link, useNavigate } from "react-router-dom";

import api from "../services/api";

export default function Register() {

    const navigate = useNavigate();

    const [name,setName]=useState("");

    const [email,setEmail]=useState("");

    const [password,setPassword]=useState("");

    const [error,setError]=useState("");

    async function register(e){

        e.preventDefault();

        try{

            await api.post("/auth/register",{

                name,

                email,

                password

            });

            navigate("/");

        }

        catch(err){

            setError(

                err.response?.data?.message ||

                "Registration failed."

            );

        }

    }

    return(

        <div className="container">

            <form className="card" onSubmit={register}>

                <h2>Create Account</h2>

                <input

                    placeholder="Name"

                    value={name}

                    onChange={(e)=>setName(e.target.value)}

                />

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

                    Register

                </button>

                {error &&

                    <p>{error}</p>

                }

                <Link to="/">

                    Already have an account?

                </Link>

            </form>

        </div>

    );

}