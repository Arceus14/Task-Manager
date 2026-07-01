import { useNavigate } from "react-router-dom";

export default function Navbar() {

    const navigate = useNavigate();

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
