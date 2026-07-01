import { useNavigate } from "react-router-dom";

import { getRole } from "../utils/auth";

export default function Navbar() {

    const navigate = useNavigate();

    const role = getRole();

    function logout() {

        localStorage.clear();

        navigate("/");

        window.location.reload();

    }

    return (

        <nav className="navbar">

            <div className="navbar-brand">

                <div className="navbar-mark">TM</div>

                <h2>Task Manager</h2>

                {role &&

                    <span className="role-badge">{role}</span>

                }

            </div>

            <button
                className="navbar-logout"
                onClick={logout}
            >

                Logout

            </button>

        </nav>

    );

}
